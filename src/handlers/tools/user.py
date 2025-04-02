# Модуль работы с пользователем

# Встроенные модули
from asyncio import Lock

# Внешние модули
from aiogram.types import Message
from loguru import logger

# Внутренние модули
from models import User

user_locks = {}
user_cached = {}

async def get_user_by_msg(msg: Message) -> User:
    global user_locks
    global user_cached
    if len(user_cached) >= 200:
        user_cached = {}
    if msg.message_id in user_cached:
        return user_cached[msg.message_id]
    if (user := await User.filter(id=msg.from_user.id).first()) is None:
        async with user_locks.get(msg.from_user.id, Lock()):
            user = await User.create(
                id=msg.from_user.id,
                name=msg.from_user.full_name,
                screen='start',
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