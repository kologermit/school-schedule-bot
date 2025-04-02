# Модуль перехода в рассылку

# Встроенные модули
from datetime import datetime

# Вешние модули
from aiogram.types import Message
from tortoise.expressions import Q

# Внутренние модули
from dispatcher import dispatcher
from .types import Context, Filter
from .tools import list_to_keyboard, handler_result
from .tools import add, delete, subscribe, back
from .schedule import get_parallel_and_symbol_by_text
from .schedule import get_student_class_buttons
from .schedule import all_student_class_variants
from models import StudentClassSubscribe, StudentClass
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
    student_class = await StudentClass.get_or_none_all(
        parallel=parallel,
        symbol=symbol,
    )
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
    student_class = await StudentClass.get_or_none_all(
        parallel=parallel,
        symbol=symbol,
    )
    if student_class is None:
        await msg.reply(answer := b('Такой класс не найден!'))
        return handler_result(delete_handler, answer)
    subscribe = await StudentClassSubscribe.get_or_none_all(
        student_class_id=student_class.id,
        user_id=ctx.user.id,
    )
    if subscribe is None:
        await msg.reply(answer := 'Подписка не найдена!')
        return handler_result(delete_handler, answer)
    subscribe.deleted = datetime.now()
    await subscribe.save()
    return handler_result(delete_handler, await to_subscribe(msg, ctx, b('Вы успешно отписались')))