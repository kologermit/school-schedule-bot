# Модуль перехода работы с расписанием

# Встроенные модули
from json import dumps
from datetime import datetime
from copy import deepcopy
from asyncio import Lock

# Вешние модули
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from loguru import logger

# Внутренние модули
from dispatcher import dispatcher, bot_async
from .tools import handler_result
from .tools import get_document_by_msg, get_sheet_by_document
from .types import Context, UpdateResult, Filter
from .tools import list_to_keyboard, schedule, cmd_reset_student_class_schedule
from .menu import to_menu
from models import ScheduleTypeEnum, WeekdayEnum
from models import StudentClass, StudentClassSchedule, StudentClassSubscribe
from modules import b
from logger import log_async_exception

schedule_screen = 'schedule:class'

# Процедура перехода в меню
@dispatcher.message(Filter(text=schedule))
async def to_schedule(msg: Message, ctx: Context) -> str:
    ctx.user.screen = schedule_screen
    buttons: dict[int, list[str]] = {}
    for c in await StudentClass.filter(deleted__isnull=True):
        buttons[c.parallel] = sorted(buttons.get(c.parallel, []) + [f'{c.parallel}{c.symbol}'])
    markup_buttons = [value for _, value in buttons.items()]
    await msg.reply(answer := b('Выбери класс'), reply_markup=list_to_keyboard(markup_buttons))
    return handler_result(to_schedule, answer)

def schedule_template(student_class: StudentClass, schedule: StudentClassSchedule) -> str:
    data: list[str] = schedule.data
    if not data:
        data = ['-']*6
    return (
        b(ScheduleTypeEnum.dict_rus[schedule.type].title())
        +b(f' расписания {WeekdayEnum.dict_rus[schedule.weekday].lower()} {student_class}:\n')
        +'\n'.join(f'{b(i+1)}. {lesson}' for i, lesson in enumerate(data))
    )


all_russian_symbols = 'ЙЦУВКАЕПНГШЩЗХЪФЫВАПРОЛДЖЭЧСМИТЬБЮ'
all_student_class_variants: set[str] = set()
for parallel in range(5, 12):
    for symbol in all_russian_symbols:
        all_student_class_variants.add(f'{parallel}{symbol}')
        
        
schedule_screen_weekday = 'schedule:weekday'
@dispatcher.message(Filter(screen=schedule_screen, text_list=all_student_class_variants))
async def to_weekday(msg: Message, ctx: Context):
    parallel = ctx.message.text[:-1]
    symbol = ctx.message.text[-1]
    student_class = await StudentClass.get_or_none(
        deleted__isnull=True,
        parallel=parallel,
        symbol=symbol,
    )
    if student_class is None:
        await msg.reply(answer := 'Класс не найден!')
        return handler_result(to_weekday, answer)
    ctx.user.screen = schedule_screen_weekday
    ctx.user.tmp_data = {'parallel': parallel, 'symbol': symbol}
    list_rus = list(map(lambda t: t.title(), WeekdayEnum.list_rus))
    
    await msg.reply(answer := b('Выбери нень недели'), reply_markup=list_to_keyboard([
        list_rus[0:3],
        list_rus[3:6],
        list_rus[6:7]
    ]))
    return handler_result(to_weekday, answer)
    

@dispatcher.message(Filter(screen=schedule_screen_weekday, text_list=WeekdayEnum.dict))
async def send_schedule(msg: Message, ctx: Context, weekday=None):
    if not weekday:
        weekday = WeekdayEnum.dict[ctx.message.text.upper()]
    else:
        weekday = WeekdayEnum.dict[weekday]
    logger.info({'weekday': weekday, 'parallel': ctx.user.tmp_data['parallel'], 'symbol': ctx.user.tmp_data['symbol']})
    student_class = await StudentClass.get_or_none(
        deleted__isnull=True,
        parallel=ctx.user.tmp_data['parallel'],
        symbol=ctx.user.tmp_data['symbol']
    )
    if student_class is None:
        return handler_result(send_schedule, await to_menu(msg, ctx, b('Класс не найден!')))

    schedule_list = await StudentClassSchedule.filter(
        deleted__isnull=True,
        student_class_id=student_class.id,
        **({} if weekday == WeekdayEnum.ALL_DAYS else {"weekday": weekday})
    )
    schedule_list = sorted(schedule_list, key=lambda sc: WeekdayEnum.list.index(sc.weekday))
    schedule_list = sorted(schedule_list, key=lambda sc: sc.type, reverse=True)
    if not schedule_list:
        answer = b('Расписание не найдено!')
    else:
        answer = '\n\n'.join(schedule_template(
            student_class, schedule) for schedule in schedule_list)
    return handler_result(send_schedule, await to_menu(msg, ctx, answer))

@log_async_exception
async def filter_cmd_send_schedule(msg: Message, **_) -> bool:
    return (
        len(split := str(msg.text).strip().upper().split(' ')) >= 2
        and split[0] in all_student_class_variants
        and ' '.join(split[1:]) in WeekdayEnum.dict
    )
@dispatcher.message(filter_cmd_send_schedule)
async def cmd_send_result(msg: Message, ctx: Context):
    split = ctx.message.text.upper().split(' ')
    parallel = split[0][:-1]
    symbol = split[0][-1]
    ctx.user.tmp_data[schedule_screen] = {'parallel': parallel, 'symbol': symbol}
    return handler_result(cmd_send_result, await send_schedule(msg, ctx, ' '.join(split[1:])))
    

@log_async_exception
async def filter_update_schedule(msg: Message, **_) -> bool:
    # Файл называется "пн изменения классы.xls"
    return (
        msg.document is not None
        and (
            (file_name := msg.document.file_name.upper().strip()).endswith('.XLS')
            or file_name.endswith('.XLSX')
        )
        and len(split := file_name.replace('.XLSX', '').replace('.XLS', '').split(' ')) >= 3
        and split[0] in WeekdayEnum.dict
        and split[1] in ScheduleTypeEnum.dict
        and split[2] in 'CLASSES,STUDENTS,КЛАССЫ,УЧЕНИКИ'
    )
student_class_lock = Lock()
@dispatcher.message(filter_update_schedule, Filter(admin=True))
async def update_schedule(msg: Message, ctx: Context):
    document = await get_document_by_msg(msg)
    sheet = get_sheet_by_document(document)
    split = document.name.split(' ')
    weekday = WeekdayEnum.dict[split[0]]
    type = ScheduleTypeEnum.dict[split[1]]
    student_class_coords: dict[tuple[int, int], StudentClass] = {}
    for x in range(1, 1000):
        for y in range(1, 1000):
            try:
                value = str(sheet.cell(x, y).value).upper().strip()
            except IndexError:
                break
            if value not in all_student_class_variants:
                continue
            parallel = value[:-1]
            symbol = value[-1]
            async with student_class_lock:
                student_class = await StudentClass.get_or_none(
                    deleted__isnull=True, 
                    parallel=parallel,
                    symbol=symbol
                )
                if student_class is None:
                    student_class = await StudentClass.create(
                        parallel=parallel,
                        symbol=symbol,
                    )
            student_class_coords[(x, y)] = student_class
    
    results: dict[str, UpdateResult] = {}
    
    for key, student_class in student_class_coords.items():
        x, y = key
        schedule_list: list[str] = []
        for i in range(8):
            schedule_list.append('')
            try:
                value1 = str(sheet.cell(x+i*2+1, y).value).strip()
                value2 = str(sheet.cell(x+i*2+2, y).value).strip()
            except IndexError:
                continue
            if len(value1) > 4:
                schedule_list[-1] = value1
            if len(value2) > 4:
                schedule_list[-1] = value2
        schedule_list = [
            (lesson if lesson else '-') 
            for i, lesson in enumerate(schedule_list) 
            if list(filter(bool, schedule_list[i:]))
        ]
        subscribers = await StudentClassSubscribe.filter(
            deleted__isnull=True,
            student_class_id=student_class.id,
        )
        async with student_class_lock:
            await StudentClassSchedule.filter(
                deleted__isnull=True,
                student_class_id=student_class.id,
                weekday=weekday,
                type=type,
            ).update(deleted=datetime.now())
            schedule = await StudentClassSchedule.create(
                student_class_id=student_class.id,
                weekday=weekday,
                data=dumps(schedule_list, indent=2, ensure_ascii=False),
                type=type
            )
        text = f'{b("Рассылка расписания!")}\n\n{schedule_template(student_class, schedule)}'
        for subscriber in subscribers:
            try:
                await bot_async.send_message(subscriber.user_id, text)
            except TelegramBadRequest:
                continue
        results[str(student_class)] = UpdateResult(
            len(subscribers),
            len(schedule.data),
        )
    answer = (
        b(f'Отчёт по рассылке {document.name}:\n')
        +'\n'.join(f'- {student_class} - Уроков: {result.count_lessons} - Подписок: {result.count_subscribers}' 
            for student_class, result in results.items())
    )
    await msg.reply(answer)
    return handler_result(update_schedule, answer)

@dispatcher.message(Filter(admin=True, text=cmd_reset_student_class_schedule))
async def reset_student_schedule(msg: Message, ctx: Context):
    student_class_filter = StudentClass.filter(deleted__isnull=True)
    student_classes = await student_class_filter
    student_class_ids = list(map(lambda sc: sc.id, student_classes))
    await student_class_filter.update(deleted=datetime.now())
    await StudentClassSchedule\
        .filter(student_class_id__in=student_class_ids)\
        .update(deleted=datetime.now())
    await StudentClassSubscribe\
        .filter(student_class_id__in=student_class_ids)\
        .update(deleted=datetime.now())
    await msg.reply(answer := 'Сброшены классы: '+', '.join(map(str, student_classes)))
    return handler_result(reset_student_schedule, answer)