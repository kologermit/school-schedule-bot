# Модуль настройки диспетчера и бота

# Внешние модули
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from telebot import TeleBot
from loguru import logger

# Внутренние модули
from config import BOT_TOKEN, BOT_START_MESSAGE, BOT_ADMINS


# Глобальные переменные для импортирования
dispatcher = Dispatcher()
bot_async = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
bot_sync = TeleBot(token=BOT_TOKEN, parse_mode='HTML')
bot_user = bot_sync.get_me()
bot_info = {
    'username': f'@{bot_user.username}',
    'name': bot_user.full_name
}

# Процедура при запуске
async def on_startup() -> None:
    if BOT_ADMINS:
        await bot_async.send_message(BOT_ADMINS[0], BOT_START_MESSAGE)

# Процедура инициализации
async def init() -> None:
    # Такое импортирование внутри процедуры нужно для замыкания
    # Чтобы не получался цикл при импортировании этого модуля
    import handlers as _
    dispatcher.startup.register(on_startup)
    
# Процедура запуска
async def run() -> None:
    await dispatcher.start_polling(bot_async)