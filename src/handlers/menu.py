# Модуль с обработчиком меню

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import handler_result, get_filter
from .tools import cmd_menu, cmd_start
from .tools import schedule, rings, holidays, info, weather, subscribe, menu
from .tools import list_to_keyboard
from .types import Context
    
menu_screen = 'menu'
menu_keyboard = list_to_keyboard([
    [schedule, rings, holidays],
    [info, weather, subscribe],
])
    
@dispatcher.message(get_filter(text_list=[menu, cmd_menu, cmd_start]))
async def to_menu(msg: Message, ctx: Context, answer=None):
    ctx.user.screen = menu_screen
    if ctx.message.text == cmd_start:
        answer = 'Привет! Я бот, который помогает узнать информацию, '
        'нужную для учёбы в ГЮЛ 86'
    elif answer is None:
        answer = 'Меню'
    await msg.reply(answer, reply_markup=menu_keyboard)
    return handler_result(to_menu, answer)