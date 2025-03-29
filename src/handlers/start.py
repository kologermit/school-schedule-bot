from aiogram.types import Message
from dispatcher import dispatcher
from .tools.handler_result import handler_result
from .tools.filters import get_filter
from .types import Context
from .screens import to_menu, start_screen

@dispatcher.message(get_filter(screen=start_screen))
async def start(msg: Message, ctx: Context):
    return handler_result(start, await to_menu(msg, ctx,
        'Привет! Я бот, который помогает узнать информацию, '
        'нужную для учёбы в ГЮЛ 86'))