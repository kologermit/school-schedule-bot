# Точка входа в программу

# Встроенные модули
from asyncio import run, create_task

# Внешние модули
from loguru import logger

# Внутренние модули
from logger import init as logger_init
from db import init as db_init
from dispatcher import init as dispatcher_init, run as dispatcher_run
from remove_schedule.student_class import init as init_remove_student_class_schedule
from remove_schedule.teacher import init as init_remove_teacher_schdule
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
    dispatcher_init()
    create_task(init_remove_student_class_schedule())
    create_task(init_remove_teacher_schdule())
    await dispatcher_run()
        
run(main())