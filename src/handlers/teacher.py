# Модуль работы с расписанием учителя

from asyncio import Lock
from datetime import datetime

from aiogram.types import Message

from dispatcher import dispatcher, bot_async
from .types import Filter, Context, UpdateResult
from .tools import handler_result
from .tools import get_document_by_msg, get_sheet_by_document, mailing
from .tools import cmd_teacher
from .schedule import filter_update_schedule, all_student_class_variants, schedule_template
from .menu import to_menu
from models import Teacher, TeacherSchedule, TeacherSubscribe, WeekdayEnum, ScheduleTypeEnum
from modules import b
from logger import log_async_exception

@dispatcher.message(Filter(pattern=f'^{cmd_teacher}.*'))
async def t(msg: Message, ctx: Context):
    split = ctx.message.text.split(' ')
    if len(split) < 2:
        await msg.reply(answer := 'Не указана фамилия!')
        return handler_result(t, answer)
    if (weekday := WeekdayEnum.dict.get(' '.join(split[3:]))) is None:
        await msg.reply(answer := b('Некорректный день недели!'))
        return handler_result(t, answer)
    teacher = await Teacher.filter_all(name__icontains=split[1]).first()
    if teacher is None:
        await msg.reply(answer := 'Учитель не найден!')
        return handler_result(t, answer)
    schedule_list = await TeacherSchedule.filter_all(
        teacher_id=teacher.id,
        **({'weekday': weekday} if weekday != WeekdayEnum.ALL_DAYS else {})
    )
    schedule_list = sorted(schedule_list, key=lambda sc: WeekdayEnum.list.index(sc.weekday))
    schedule_list = sorted(schedule_list, key=lambda sc: sc.type, reverse=True)
    if not schedule_list:
        answer = b('Расписание не найдено!')
    else:
        answer = '\n\n'.join(schedule_template(
            teacher, schedule) for schedule in schedule_list)
    return handler_result(t, await to_menu(msg, ctx, answer))

    
@log_async_exception
async def filter_update_teacher_schedule(msg: Message, **_):
    return (
        msg.document is not None
        and any(l in msg.document.file_name.upper() for l in [
            'УЧИТЕЛЬ', 'УЧИТЕЛЯ',
            'TEACHER', 'TEACHERS',
        ])
    )
teacher_lock = Lock()
@dispatcher.message(filter_update_schedule,
    filter_update_teacher_schedule, 
    Filter(admin=True))
async def update_teacher_schedule(msg: Message, ctx: Context):
    document = await get_document_by_msg(msg)
    sheet = get_sheet_by_document(document)
    split = document.name.split(' ')
    weekday = WeekdayEnum.dict[split[0]]
    type = ScheduleTypeEnum.dict[split[1]]
    
    # Этап 1: Нахождение всех учителей и синхронизация с БД
    teacher_coords: dict[tuple[int, int], Teacher] = {}
    for row in range(1000):
        for col in range(1000):
            try:
                value = str(sheet.cell(row, col).value).upper().strip().replace(',', '.')
            except IndexError:
                continue
            if value.count('.') < 2:
                continue
            value = value.replace('.', ' ').strip()
            async with teacher_lock:
                teacher = await Teacher.filter_all(name=value).first()
                if teacher is None:
                    teacher = await Teacher.create(name=value)
            teacher_coords[(row, col)] = teacher
            
    # Этап 2: Нахождение расписания
    teacher_schedules: list[tuple[Teacher, TeacherSchedule]] = []
    for (row, col), teacher in teacher_coords.items():
        schedule_list: list[str] = ['']*8
        for i in range(8):
            for j in range(-1, 2):
                try:
                    v = str(sheet.cell(row, col+j+i*2+1).value).upper().strip()
                except IndexError:
                    continue
                if v in all_student_class_variants:
                    schedule_list[i] = v
        schedule_list = [
            (lesson if lesson else '-') 
            for i, lesson in enumerate(schedule_list) 
            if list(filter(bool, schedule_list[i:]))
        ]
        teacher_schedules.append((teacher, TeacherSchedule(
            teacher_id=teacher.id,
            weekday=weekday,
            data=schedule_list,
            type=type
        )))
    
    # Этап 3: Сохранение в БД и рассылка
    results: dict[str, UpdateResult] = {}
    await TeacherSchedule.filter_all(
        teacher_id__in=(t.id for t, _ in teacher_schedules),
        weekday=weekday,
        type=type,
    ).update(deleted=datetime.now())
    await TeacherSchedule.bulk_create(s for _, s in teacher_schedules)
    for teacher, schedule in teacher_schedules:
        subscribers = await TeacherSubscribe\
            .filter_all(teacher_id=teacher.id)\
            .values_list('user_id', flat=True)
        text = b("Рассылка расписания учителя!\n\n")+schedule_template(teacher, schedule)
        await mailing(text, subscribers, bot_async)
        results[teacher.name] = UpdateResult(
            len(subscribers),
            len(schedule.data),
        )
    
    await msg.reply(answer := UpdateResult.results_to_text(document.name, results))
    return handler_result(update_teacher_schedule, answer)
    
        
        
    