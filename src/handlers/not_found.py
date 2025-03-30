# Модуль не найденных сообщений

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools.filters import get_filter
from .tools.handler_result import handler_result

# Последний возможный обработчик с ответом пользователю
@dispatcher.message(get_filter())
async def not_found(msg: Message):
    await msg.answer(answer := 'Не понял!')
    return handler_result(not_found, answer)
    
# Последний обработчик вообще, чтобы отработал мидлвар
@dispatcher.message()
async def skip(_):
    return handler_result(skip, None)