# Модуль с обработчиком старта

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import handler_result
from .tools import get_filter
from .tools import schedule
from .types import Context
from .screens import menu_buttons, menu_screen
from .screens import to_schedule

@dispatcher.message(get_filter(screen=menu_screen, text_list=menu_buttons))
async def menu(msg: Message, ctx: Context):
    return handler_result(menu, await {
        schedule: to_schedule, 
    }[ctx.message.text](msg, ctx))