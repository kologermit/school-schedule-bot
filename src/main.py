# Встроенные модули
from asyncio import run

# Внешние модули
from loguru import logger

# Внутренние модули
from logger import init as logger_init
from config import (
    PROJECT_NAME, 
    LOGS_DIR, 
    BOT_TOKEN, 
    BOT_ADMINS
)

async def main():
    logger_init(LOGS_DIR, PROJECT_NAME, BOT_TOKEN, BOT_ADMINS)
        
run(main())