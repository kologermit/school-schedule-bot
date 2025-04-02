# Модуль работы с расписанием учителя

from asyncio import Lock
from datetime import datetime

from aiogram.types import Message

from dispatcher import dispatcher, bot_async
from .types import Filter, Context, UpdateResult
from .tools import handler_result
from .tools import get_document_by_msg, get_sheet_by_document, mailing
from .tools import cmd_teacher, cmd_teacher_subscribe, cmd_teachet_unsubscribe, cmd_reset_teacher_schedule
from .schedule import filter_update_schedule, all_student_class_variants, schedule_template
from .menu import to_menu
from models import Teacher, TeacherSchedule, TeacherSubscribe, WeekdayEnum, ScheduleTypeEnum
from modules import b
from logger import log_async_exception

@dispatcher.message(Filter(pattern=f'^{cmd_teacher} .*'))
async def t(msg: Message, ctx: Context):
    split = ctx.message.text.split(' ')
    if len(split) < 2:
        await msg.reply(answer := 'Не указана фамилия!')
        return handler_result(t, answer)
    if (weekday := WeekdayEnum.dict.get(' '.join(split[2:]).upper())) is None:
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


@dispatcher.message(Filter(pattern=f'^{cmd_teacher_subscribe} .*'))
async def ts(msg: Message, ctx: Context):
    teacher = await Teacher.filter_all(
        name__icontains=ctx.message.text.replace(cmd_teacher_subscribe, '').upper().strip())\
        .first()
    if teacher is None:
        await msg.reply(answer := b('Учитель не найден!'))
        return handler_result(ts, answer)
    subscribe = await TeacherSubscribe.filter_all(user_id=ctx.user.id, teacher_id=teacher.id).first()
    if subscribe:
        await msg.reply(answer := b('Вы уже подписаны!'))
        return handler_result(ts, answer)
    await TeacherSubscribe.create(
        user_id=ctx.user.id,
        teacher_id=teacher.id
    )
    await msg.reply(answer := b('Вам успешно подписались на ' + teacher.name.title()))
    return handler_result(ts, answer)
    
@dispatcher.message(Filter(pattern=f'^{cmd_teachet_unsubscribe} .*'))
async def tu(msg: Message, ctx: Context):
    teacher = await Teacher.filter_all(
        name__icontains=ctx.message.text.replace(cmd_teachet_unsubscribe, '').upper().strip())\
        .first()
    if teacher is None:
        await msg.reply(answer := b('Учитель не найден!'))
        return handler_result(tu, answer)
    subscribe = await TeacherSubscribe.filter_all(user_id=ctx.user.id, teacher_id=teacher.id).first()
    if subscribe is None:
        await msg.reply(answer := b('Вы не подписаны!'))
        return handler_result(tu, answer)
    subscribe.deleted = datetime.now()
    await subscribe.save()
    await msg.reply(answer := b('Вы отписались от '+teacher.name.title()))
    return handler_result(tu, answer)
    
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
    
        
@dispatcher.message(Filter(admin=True, text=cmd_reset_teacher_schedule))
async def reset_teacher_schedule(msg: Message, ctx: Context):
    teachers = await Teacher.filter_all()
    teacher_ids = await Teacher.filter_all().values_list('id', flat=True)
    await Teacher.filter_all().update(deleted=datetime.now())
    await TeacherSchedule\
        .filter_all(teacher_id__in=teacher_ids)\
        .update(deleted=datetime.now())
    user_ids = await TeacherSubscribe\
        .filter_all(teacher_id__in=teacher_ids).values_list('user_id', flat=True)
    await TeacherSubscribe.filter_all(user_id__in=user_ids).update(deleted=datetime.now())
    await mailing('Ваша рассылка на расписание сброшена. Подпишитесь на нужного учителя снова', 
        user_ids, bot_async)
    await msg.reply(answer := 'Сброшены учителя: '+', '.join(map(str, teachers)))
    return handler_result(reset_teacher_schedule, answer)