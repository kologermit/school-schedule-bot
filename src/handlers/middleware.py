# Мидлвар. Запускается перед обработкой сообщения
# Создает сообщение и пользователя в БД
# Логгирует информацию о пришедшем сообщении
# Передаёт в обработчик контекст

# Встроенные модули
from typing import Awaitable, Callable

# Внешние модули
from aiogram.types import TelegramObject
from aiogram.types import Message as TGMessage
from loguru import logger

# Внутренние модули
from .tools.user import get_user_by_msg
from .types import Context
from models import Message
from logger import log_async_exception
from dispatcher import dispatcher, bot_async

# Общий мидлвар
@log_async_exception
async def middleware(
    handler: Callable[[TelegramObject, dict[str, any]], Awaitable[any]],
    event: TelegramObject,
    data: dict[str, any]
) -> any:
    # Получение необходимых данных из сообщения
    
    if isinstance(event, TGMessage):
        msg = event
    else:
        raise TypeError('unsupperted event type')
    
    user = await get_user_by_msg(msg) 
    if (message := await Message.get_or_none(id=msg.message_id, user_id=user.id)) is None:
        message = await Message.create(
            id=msg.message_id,
            user_id=msg.from_user.id,
            text=str(msg.text.strip() if msg.text else msg.caption),
        )
    
    # Добавление данных в контекст, 
    # который будет позже использован в обработчике
    data['ctx'] = Context(
        user=user,
        message=message,
    )

    # Отключение уведомления об отправленных сообщениях
    data['disable_notification'] = True

    # Формирование данных для логгирования
    log = {
        'event': type(event),
        'user': {'id': user.id, 'name': user.name, 'screen': user.screen},
        'message': {
            "id":message.id,
            "text": message.text,
        },
    }

    # Запуск обработчика
    @log_async_exception
    async def run_event(event, data):
        return await handler(event, data)
    log['result'] = await run_event(event, data)
    if isinstance(log['result'], Exception):
        await bot_async.send_message(user.id, 'Произошла ошибка')
    
    logger.info(log)
    await user.save()
    return log['result']

# Добавление мидлвара к обработчикам сообщений и колбеков
dispatcher.message.middleware(middleware)