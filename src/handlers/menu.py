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
from .subscribe import subscribe_screen
from .schedule import schedule_screen
    
menu_screen = 'menu'
menu_keyboard = list_to_keyboard([
    [schedule, rings, holidays],
    [info, weather, subscribe],
])
    
@dispatcher.message(get_filter(text_list=[menu, cmd_menu, cmd_start]))
async def to_menu(msg: Message, ctx: Context):
    ctx.user.screen = menu_screen
    await msg.answer(answer := ('Привет! Я бот, который помогает узнать информацию, '
        'нужную для учёбы в ГЮЛ 86' if ctx.message.text == cmd_start else 'Меню'), 
        reply_markup=menu_keyboard)
    return handler_result(to_menu, answer)