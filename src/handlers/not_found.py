# Модуль не найденных сообщений

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import handler_result
from .types import Filter

# Последний возможный обработчик с ответом пользователю
@dispatcher.message(Filter())
async def not_found(msg: Message):
    await msg.reply(answer := 'Не понял!')
    return handler_result(not_found, answer)
    
# Последний обработчик вообще, чтобы отработал мидлвар
@dispatcher.message()
async def skip(_):
    return handler_result(skip, None)