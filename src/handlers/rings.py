# Модуль с обработчиком звонков

# Встроенные модули
from datetime import time, datetime
from re import match

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from models import Ring
from modules import b, time_template
from logger import log_async_exception
from .tools import get_filter, handler_result
from .tools import cmd_new_rings, rings
from .types import Context
    
    
@dispatcher.message(get_filter(text=rings))
async def rings_handler(msg: Message, ctx: Context):
    rings = await Ring.filter(deleted__isnull=True).order_by('start')
    answer = b("Раписание звонков:\n")+'\n'.join(
        f'{b(i+1)}. {ring.start.strftime(time_template)}-{ring.end.strftime(time_template)}'
        for i, ring in enumerate(rings))
    await msg.answer(answer)
    return handler_result(rings_handler, answer)


# /new_rings
# 08:20-09:10
# 09:20-10:10
# ...
@log_async_exception
async def filter_new_rings(msg: Message, **_) -> bool:
    split = str(msg.text).strip().split('\n')
    return (
        len(split) >= 2
        and split[0] == cmd_new_rings
        and len(
            filter(
                lambda line: match("^(\d+):(\d+)-(\d+):(\d+).*", line),
                split[1:]
            )
        ) == len(split)-1
    )
    
@dispatcher.message(get_filter(admin=True), filter_new_rings)
async def new_rings(msg: Message, ctx: Context):
    split = ctx.message.text.split('\n')
    rings = []
    for line in split[1:]:
        try:
            start = time.fromisoformat(line.split('-')[0].strip())
            end = time.fromisoformat(line.split('-')[1].strip())
        except ValueError:
            await msg.answer(answer := f'В строке {line} не правильно указано время')
            return handler_result(new_rings, answer)
        rings.append(Ring(start=start, end=end))
    await Ring.filter(deleted__isnull=True).update(deleted=datetime.now())
    await Ring.bulk_create(rings)
    await msg.answer(answer := 'Создано расписание звонков')
    answer += str(await rings_handler(msg, ctx))
    return handler_result(new_rings, answer)