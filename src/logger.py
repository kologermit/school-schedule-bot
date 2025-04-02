# Модуль настройки логгера

# Встроенные модули
from os import path, environ
from uuid import uuid4 as uuid
from datetime import datetime
from typing import Callable

# Внешние модули
from loguru import logger
from telebot import TeleBot

# Внутренние модули
from modules import b, pre, datetime_template
from modules import create_dir_if_not_exists
from modules import send_to_admin

# Глобальные переменные, которые меняются при инициации
bot = None
admins = []
service = None

# Процедура подготовки логгера
def init(logs_dir: str='', 
    service_name: str='defaultservice', 
    bot_token: str='', 
    tg_admins: list[int]=[]) -> None:
    
    # Обновление глобальных переменных
    global bot
    global admins
    global service
    bot = TeleBot(bot_token) if bot_token else None
    service = service_name
    admins = tg_admins
    
    # Отключение буффера для вывода в stdout
    environ['PYTHONUNBUFFERED']='1'

    # Если в конфиге указана папка для логов,
    # то будет создана эта папка.
    # И файлы лога будут создаваться каждый день
    if logs_dir:
        create_dir_if_not_exists(logs_dir)
        logger.add(
            path.join(logs_dir, service+'-{time:YYYY-MM-DD}.log'), 
            rotation='00:00',
            serialize=True, 
            level='INFO', 
            backtrace=True, 
            diagnose=True,
        )
        logger.info({'event': 'INIT_LOGS_DIR', 'log_path': logs_dir})

# Общая функция для лога ошибки и рассылки сообщения админам
def log_err_with_code_and_send_message(err: Exception) -> str:
    code = str(uuid())
    logger.exception(code, err)
    if bot:
        try:
            now = datetime.now()
            send_to_admin(
                f"{b('Произошла ошибка:')}\n"
                f'{b("- Сервис:")} {pre(service)}\n'
                f'{b("- Код:")} {pre(code)}\n'
                f'{b("- Ошибка:")} {pre(err).replace("<", "[").replace(">", "]")}\n'
                f'{b("- Время:")} {pre(now.strftime(datetime_template))}', bot, admins)
        except Exception as err2:
            logger.exception(err2)
    return code

# Декоратор для отлова любых ошибок
def log_sync_exception(f: Callable) -> Callable:
    def _(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as err:
            log_err_with_code_and_send_message(err)
            return err
    return _

# Декоратор для отлова любых ошибок в асинхронных функциях
def log_async_exception(f: Callable) -> Callable:
    async def _(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as err:
            log_err_with_code_and_send_message(err)
            return err
    return _