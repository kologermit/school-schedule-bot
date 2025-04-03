# Модуль перехода в рассылку

# Встроенные модули
from datetime import datetime

# Вешние модули
from aiogram.types import Message
from tortoise.expressions import Q

# Внутренние модули
from dispatcher import dispatcher, bot_async
from .types import Context, Filter
from .tools import list_to_keyboard, handler_result, mailing
from .tools import add, delete, subscribe, back
from .tools import cmd_mailing, cmd_mailing_student_classes, cmd_mailing_teachers
from .schedule import get_parallel_and_symbol_by_text
from .schedule import get_student_class_buttons
from .schedule import all_student_class_variants
from models import StudentClassSubscribe, StudentClass, User, TeacherSubscribe
from modules import b

subscribe_screen = 'subscribe'
subscribe_add_screen = 'subscribe:add'
subscribe_delete_screen = 'subscribe:delete'

# Процедура перехода в меню

@dispatcher.message(Filter(screen_list=[subscribe_add_screen, subscribe_delete_screen], text=back))
@dispatcher.message(Filter(text=subscribe))
async def to_subscribe(msg: Message, ctx: Context, answer='') -> str:
    subscribes = await StudentClassSubscribe.filter_all(user_id=ctx.user.id)
    if not answer and ctx.message.text == back:
        answer = 'Меню'
    elif not answer:
        student_classes = await StudentClass.filter_all(
            id__in=map(lambda s: s.student_class_id, subscribes))
        answer = b('Вы не подписаны на расписание')
        if student_classes:
            answer = b('Вы получаете раписание:\n') + \
                '\n'.join(f'{i+1}. {sc.parallel}{sc.symbol}' 
                    for i, sc in enumerate(student_classes))
    await msg.reply(answer, reply_markup=list_to_keyboard([
        [add, delete],
    ]))
    ctx.user.screen = subscribe_screen
    return handler_result(to_subscribe, answer)

@dispatcher.message(Filter(screen=subscribe_screen, text=add))
async def to_add(msg: Message, ctx: Context):
    ctx.user.screen = subscribe_add_screen
    student_class_ids = await StudentClassSubscribe.filter_all(
        user_id=ctx.user.id).values_list('student_class_id', flat=True)
    student_classes = await StudentClass.filter_all(~Q(id__in=student_class_ids))
    buttons = get_student_class_buttons(student_classes)
    buttons.append([back])
    await msg.reply(answer := b('Выбери класс:'), reply_markup=list_to_keyboard(buttons))
    return handler_result(to_add, answer)


@dispatcher.message(Filter(screen=subscribe_add_screen, text_list=all_student_class_variants))
async def add_handler(msg: Message, ctx: Context):
    parallel, symbol = get_parallel_and_symbol_by_text(ctx.message.text)
    student_class = await StudentClass.filter_all(
        parallel=parallel,
        symbol=symbol,
    ).first()
    if student_class is None:
        await msg.reply(answer := b('Класс не найден!'))
        return handler_result(add_handler, answer)
    await StudentClassSubscribe.create(user_id=ctx.user.id, student_class_id=student_class.id)
    return handler_result(add_handler, await to_subscribe(msg, ctx, b('Вы успешно подписались')))
    

@dispatcher.message(Filter(screen=subscribe_screen, text=delete))
async def to_delete(msg: Message, ctx: Context):
    student_class_ids = await StudentClassSubscribe.filter_all(user_id=ctx.user.id)\
        .values_list('student_class_id', flat=True)
    student_classes = list(map(str, await StudentClass.filter_all(id__in=student_class_ids)))
    if not student_classes:
        await msg.reply(answer := b('Чтобы отменить подписку, нужно сначала подписаться!'))
        return handler_result(to_delete, answer)
    ctx.user.screen = subscribe_delete_screen
    await msg.reply(answer := b('Выбери класс:'), 
        reply_markup=list_to_keyboard([student_classes, [back]]))
    return handler_result(to_delete, answer)
    
@dispatcher.message(Filter(screen=subscribe_delete_screen, text_list=all_student_class_variants))
async def delete_handler(msg: Message, ctx: Context):
    parallel, symbol = get_parallel_and_symbol_by_text(ctx.message.text)
    student_class = await StudentClass.filter_all(
        parallel=parallel,
        symbol=symbol,
    ).first()
    if student_class is None:
        await msg.reply(answer := b('Такой класс не найден!'))
        return handler_result(delete_handler, answer)
    subscribe = await StudentClassSubscribe.filter_all(
        student_class_id=student_class.id,
        user_id=ctx.user.id,
    ).first()
    if subscribe is None:
        await msg.reply(answer := 'Подписка не найдена!')
        return handler_result(delete_handler, answer)
    subscribe.deleted = datetime.now()
    await subscribe.save()
    return handler_result(delete_handler, await to_subscribe(msg, ctx, b('Вы успешно отписались')))

@dispatcher.message(Filter(admin=True, 
    pattern=f'^({cmd_mailing}|{cmd_mailing_teachers}|{cmd_mailing_student_classes}).*'))
async def mailing_handler(msg: Message, ctx: Context):
    text = ctx.message.text.replace(cmd_mailing_teachers, '').strip()
    text = ctx.message.text.replace(cmd_mailing_student_classes, '').strip()
    text = ctx.message.text.replace(cmd_mailing, '').strip()
    if not text:
        await msg.reply(answer := b('Нет сообщения для рассылки!'))
        return handler_result(mailing_handler, answer)
    if cmd_mailing_teachers in ctx.message.text:
        text = b('Рассылка учителям:\n\n') + text
        user_ids = await TeacherSubscribe.filter_all().values_list('user_id', flat=True)
    elif cmd_mailing_student_classes in ctx.message.text:
        text = b('Рассылка ученикам:\n\n') + text
        user_ids = await StudentClassSubscribe.filter_all().values_list('user_id', flat=True)
    else:
        text = b('Общая рассылка:\n\n') + text
        user_ids = await User.filter().values_list('id', flat=True)
    await mailing(text, user_ids, bot_async)
    await msg.reply(answer := b(f'Отправлено сообщений: {len(user_ids)}'))
    return handler_result(mailing_handler, answer)