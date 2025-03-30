# Модуль перехода в меню

# Вешние модули
from aiogram.types import Message

# Внутренние модули
from handlers.types import Context
from handlers.tools import menu, back, list_to_keyboard
from handlers.tools import handler_result
from models import StudentClass
schedule_screen = 'schedule'

# Процедура перехода в меню
async def to_schedule(msg: Message, ctx: Context) -> str:
    ctx.user.screen = schedule_screen
    buttons: dict[int, list[str]] = {}
    for c in await StudentClass.filter(deleted__isnull=True):
        buttons[c.parallel] = sorted(buttons.get(c.parallel, []) + [f'{c.parallel}{c.symbol}'])
    markup_buttons: list[list[str]] = [value for _, value in buttons.items()]
    markup_buttons.append([back, menu])
    
    await msg.answer(answer := 'Выбери класс', reply_markup=list_to_keyboard(markup_buttons))
    return answer