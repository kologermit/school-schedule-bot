from aiogram.types import Message
from asyncio import Lock
from loguru import logger
from models import User
from config import BOT_ADMINS
from handlers.screens import start_screen

user_locks = {}
user_cached = {}

async def get_user_by_msg(msg: Message) -> User:
    global user_locks
    global user_cached
    if len(user_cached) >= 200:
        user_cached = {}
    if msg.message_id in user_cached:
        return user_cached[msg.message_id]
    if (user := await User.get_or_none(id=msg.from_user.id)) is None:
        async with user_locks.get(msg.from_user.id, Lock()):
            user = await User.create(
                id=msg.from_user.id,
                name=msg.from_user.full_name,
                screen=start_screen,
            )
            logger.info({
                'event': 'NEW_USER',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    
                }
            })
    user_cached[msg.message_id] = user
    return user