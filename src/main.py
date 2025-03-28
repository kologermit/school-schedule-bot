# Точка входа в программу

# Встроенные модули
from asyncio import run

# Внешние модули
from loguru import logger

# Внутренние модули
from logger import init as logger_init
from db import init as db_init
from config import (
    PROJECT_NAME, 
    LOGS_DIR, 
    BOT_TOKEN, 
    BOT_ADMINS,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

async def main():
    logger_init(LOGS_DIR, PROJECT_NAME, BOT_TOKEN, BOT_ADMINS)
    await db_init(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        
run(main())