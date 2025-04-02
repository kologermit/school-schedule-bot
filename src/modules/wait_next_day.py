from asyncio import sleep
from datetime import datetime, timedelta
from loguru import logger

async def wait_next_day(description: str) -> tuple[datetime, datetime]:
    now = datetime.now()
    end = datetime(now.year, now.month, now.day, 0, 0, 0) + timedelta(days=1)
    seconds = (end-now).seconds+5
    logger.info({'event': 'SLEEP_BEFORE_NEXT_DAY', 'description': description, 'seconds': seconds})
    await sleep(seconds)
    return now, datetime.now()