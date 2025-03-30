# Модуль с обработчиком меню

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import handler_result
from .tools import get_filter
from .tools import schedule, subscribe, menu, rings
from .types import Context
from .screens import menu_buttons, menu_screen, to_menu
from .screens import to_schedule
from .screens import to_subscribe
from .rings import rings_handler
    
@dispatcher.message(get_filter(text_list=[menu, '/menu']))
async def cmd_menu(msg: Message, ctx: Context):
    return handler_result(cmd_menu, await to_menu(msg, ctx))

@dispatcher.message(get_filter(screen=menu_screen, text_list=menu_buttons))
async def menu_handler(msg: Message, ctx: Context):
    return handler_result(menu_handler, await {
        schedule: to_schedule, 
        subscribe: to_subscribe,
        rings: rings_handler
    }[ctx.message.text](msg, ctx))