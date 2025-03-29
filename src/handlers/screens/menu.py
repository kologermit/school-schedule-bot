from aiogram.types import Message
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
menu_keyboard = list_to_keyboard([
    [schedule, rings, holidays],
    [info, ph_culture, settings],
    [menu]
])

async def to_menu(msg: Message, ctx: Context, answer='Меню'):
    ctx.user.screen = menu_screen
    await msg.answer(answer, reply_markup=menu_keyboard)
    return answer