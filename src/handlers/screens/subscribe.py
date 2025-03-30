# Модуль перехода в меню

# Вешние модули
from aiogram.types import Message

# Внутренние модули
from handlers.types import Context
from handlers.tools import menu, back, list_to_keyboard
from handlers.tools import add, delete
from models import StudentClassSubscribe, StudentClass

subscribe_screen = 'subscribe'

# Процедура перехода в меню
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
    
    answer = 'Вы не подписаны на расписание'
    if student_classes:
        answer = 'Вы получаете раписание:\n'+ \
            '\n'.join(f'{i+1}. {sc.parallel}{sc.symbol}' for i, sc in enumerate(student_classes))
    
    
    await msg.answer(answer, reply_markup=list_to_keyboard([
        [add, delete],
        [back, menu],
    ]))
    return answer

