from copy import deepcopy
from re import match
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType
from aiogram.filters import BaseFilter
from logger import log_async_exception
from config import BOT_ADMINS
from handlers.tools import get_user_by_msg

class Filter(BaseFilter):
    text: str
    text_list: list[str]
    text_upper: bool
    pattern: str
    screen: str
    screen_list: list[list]
    admin: bool
    def __init__(self,
        text="",
        text_list: list[str]=[],
        text_upper=True,
        pattern="",
        screen="",
        screen_list: list[str]=[],
        admin=False
    ):
        super().__init__()
        if text_upper:
            self.text =         deepcopy(text)
            self.text_list =    deepcopy(text_list)
            self.text_upper =   deepcopy(text_upper)
            self.pattern =      deepcopy(pattern)
            self.screen =       deepcopy(screen)
            self.screen_list =  deepcopy(screen_list)
            self.admin =        deepcopy(admin)
            if self.text_upper:
                self.text = self.text.upper()
                self.text_list = list(map(lambda t: t.upper(), self.text_list))
                self.pattern = self.pattern.upper()
        
    @log_async_exception
    async def __call__(self, msg: Message, **_) -> bool:
        msg_text = str(msg.text).strip()
        if self.text_upper:
            msg_text = msg_text.upper()
        user = await get_user_by_msg(msg)
        return (
            msg.chat.type in [ChatType.PRIVATE.value, ChatType.SENDER.value]
            and (not self.text        or msg_text == self.text                    )
            and (not self.text_list   or msg_text in self.text_list               )
            and (not self.pattern     or match(self.pattern, msg_text) is not None)
            and (not self.admin       or user.id in BOT_ADMINS                    )
            and (not self.screen      or user.screen == self.screen               )
            and (not self.screen_list or user.screen in self.screen_list          )
        )