from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

async def mailing(text: str, user_ids: list[int], bot: Bot):
    for id in user_ids:
        try:
            await bot.send_message(id, text)
        except TelegramBadRequest:
            continue