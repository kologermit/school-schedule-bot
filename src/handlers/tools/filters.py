# Модуль фильтров сообщений

# Встроенные модули
from re import match
from typing import Awaitable

# Внешнеи модули
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType

# Внутренние модули
from logger import log_async_exception
from .user import get_user_by_msg
from config import BOT_ADMINS

def get_filter(
    text="",
    text_list: list[str]=[],
    text_upper=True,
    pattern="",
    screen="",
    screen_list: list[str]=[],
    admin=False
) -> Awaitable:
    if text_upper:
        text = text.upper()
        text_list = list(map(lambda t: t.upper(), text_list))
    @log_async_exception
    async def filt(msg: Message, **_) -> bool:
        msg_text = str(msg.text).strip()
        if text_upper:
            msg_text = msg_text.upper()
        user = await get_user_by_msg(msg)
        return (
            msg.chat.type in [ChatType.PRIVATE.value, ChatType.SENDER.value]
            and (not text           or msg_text == text                     )
            and (not text_list      or msg_text in text_list                )
            and (not pattern        or match(pattern, msg_text) is not None )
            and (not admin          or user.id in BOT_ADMINS                )
            and (not screen         or user.screen == screen                )
            and (not screen_list    or user.screen in screen_list           )
        )
    return filt