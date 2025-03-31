# Модуль с обработчиком меню

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import handler_result, get_filter
from .tools import schedule, subscribe, menu, rings, holidays, info, weather, cmd_menu, cmd_start
from .types import Context
from .screens import menu_buttons, menu_screen, to_menu
from .screens import to_schedule, to_subscribe
from .rings import rings_handler
from .holidays import holidays_handler
from .info import info_handler
from .weather import weather_handler
    
@dispatcher.message(get_filter(text_list=[menu, cmd_menu, cmd_start]))
async def cmd_menu(msg: Message, ctx: Context):
    return handler_result(cmd_menu, await to_menu(msg, ctx))

@dispatcher.message(get_filter(screen=menu_screen, text_list=menu_buttons))
async def menu_handler(msg: Message, ctx: Context):
    return handler_result(menu_handler, await {
        schedule: to_schedule, 
        subscribe: to_subscribe,
        rings: rings_handler,
        holidays: holidays_handler,
        info: info_handler,
        weather: weather_handler
    }[ctx.message.text](msg, ctx))