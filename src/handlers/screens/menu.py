# Модуль перехода в меню

# Вешние модули
from aiogram.types import Message

# Внутренние модули
from handlers.types import Context
from handlers.tools.buttons import (
    list_to_keyboard,
    schedule,
    rings,
    holidays,
    info,
    ph_culture,
    settings,
    menu
)

menu_screen = 'menu'
menu_buttons = [
    schedule, rings, holidays,
    info, ph_culture, settings,
    menu
]
menu_keyboard = list_to_keyboard([
    menu_buttons[0:3],
    menu_buttons[3:6],
    menu_buttons[6:7]
])

# Процедура перехода в меню
async def to_menu(msg: Message, ctx: Context, answer='Меню') -> str:
    ctx.user.screen = menu_screen
    await msg.answer(answer, reply_markup=menu_keyboard)
    return answer