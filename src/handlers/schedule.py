# Модуль перехода работы с расписанием

# Встроенные модули
from json import dumps
from datetime import datetime
from copy import deepcopy

# Вешние модули
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

# Внутренние модули
from dispatcher import dispatcher, bot_async
from .tools import get_filter, handler_result
from .tools import get_document_by_msg, get_sheet_by_document
from .types import Context, ScheduleTypeEnum, WeekdayEnum, UpdateResult
from .tools import list_to_keyboard, schedule
from models import StudentClass, StudentClassSchedule, StudentClassSubscribe
from modules import b
from logger import log_async_exception

schedule_screen = 'schedule'

# Процедура перехода в меню
@dispatcher.message(get_filter(text=schedule))
async def to_schedule(msg: Message, ctx: Context) -> str:
    ctx.user.screen = schedule_screen
    buttons: dict[int, list[str]] = {}
    for c in await StudentClass.filter(deleted__isnull=True):
        buttons[c.parallel] = sorted(buttons.get(c.parallel, []) + [f'{c.parallel}{c.symbol}'])
    markup_buttons = [value for _, value in buttons.items()]
    await msg.answer(answer := b('Выбери класс'), reply_markup=list_to_keyboard(markup_buttons))
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
        and await get_filter(admin=True)(msg)
    )
@dispatcher.message(filter_update_schedule)
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
        subscribers = await StudentClassSubscribe.filter(
            deleted__isnull=True,
            student_class_id=student_class.id,
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