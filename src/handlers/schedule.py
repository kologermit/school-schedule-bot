# Модуль перехода работы с расписанием

# Вешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import get_filter, handler_result
from .types import Context
from .tools import list_to_keyboard, schedule
from models import StudentClass
from modules import b

schedule_screen = 'schedule'

# Процедура перехода в меню
@dispatcher.message(get_filter(text=schedule))
async def to_schedule(msg: Message, ctx: Context) -> str:
    ctx.user.screen = schedule_screen
    buttons: dict[int, list[str]] = {}
    for c in await StudentClass.filter(deleted__isnull=True):
        buttons[c.parallel] = sorted(buttons.get(c.parallel, []) + [f'{c.parallel}{c.symbol}'])
    markup_buttons: list[list[str]] = [value for _, value in buttons.items()]
    
    await msg.answer(answer := b('Выбери класс'), reply_markup=list_to_keyboard(markup_buttons))
    return handler_result(to_schedule, answer)