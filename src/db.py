# Модуль настройки БД

# Внешние модули
from tortoise import Tortoise
from loguru import logger

# Процедура подготовки БД
async def init(
        host='localhost', 
        port='5432', 
        db='bot', 
        user='postgres', 
        password='qwerty', 
        models='models'
    ):
    # Настройка подключения к БД
    # И настройка моделей
    url = f'postgres://{user}:{password}@{host}:{port}/{db}'
    logger.info({
        'event': 'INIT_DB_CONNECTION', 
        'user': user, 
        'db': db, 
        'host': host,
        'port': port
    })
    await Tortoise.init(
        db_url=url,
        modules={'models': [models]}
    )
    await Tortoise.generate_schemas()