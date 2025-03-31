# Модуль перехода в рассылку

# Вешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .types import Context
from .tools import get_filter, handler_result
from .tools import list_to_keyboard
from .tools import add, delete, subscribe
from models import StudentClassSubscribe, StudentClass
from modules import b

subscribe_screen = 'subscribe'

# Процедура перехода в меню

@dispatcher.message(get_filter(text=subscribe))
async def to_subscribe(msg: Message, ctx: Context) -> str:
    ctx.user.screen = subscribe_screen
    
    subscribes = await StudentClassSubscribe.filter(
        user_id=ctx.user.id,
        deleted__isnull=True
    )
    student_classes = await StudentClass.filter(
        id__in=map(lambda s: s.student_class_id, subscribes),
        deleted__isnull=True
    )
    
    answer = b('Вы не подписаны на расписание')
    if student_classes:
        answer = b('Вы получаете раписание:\n') + \
            '\n'.join(f'{i+1}. {sc.parallel}{sc.symbol}' for i, sc in enumerate(student_classes))
    
    
    await msg.answer(answer, reply_markup=list_to_keyboard([
        [add, delete],
    ]))
    return handler_result(to_subscribe, answer)

