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
from .tools import handler_result
from .tools import cmd_new_rings, rings
from .types import Context, Filter
    
    
@dispatcher.message(Filter(text=rings))
async def rings_handler(msg: Message, ctx: Context):
    rings = await Ring.filter(deleted__isnull=True).order_by('start')
    answer = b("Раписание звонков:\n")+'\n'.join(
        f'{b(i+1)}. {ring.start.strftime(time_template)}-{ring.end.strftime(time_template)}'
        for i, ring in enumerate(rings))
    await msg.reply(answer)
    return handler_result(rings_handler, answer)


# /new_rings
# 08:20-09:10
# 09:20-10:10
# ...
@dispatcher.message(Filter(admin=True, pattern=f'.*{cmd_new_rings}.*'))
async def new_rings(msg: Message, ctx: Context):
    split = ctx.message.text.split('\n')
    rings = []
    for line in split[1:]:
        try:
            start = time.fromisoformat(line.split('-')[0].strip())
            end = time.fromisoformat(line.split('-')[1].strip())
        except ValueError:
            await msg.reply(answer := f'В строке {line} не правильно указано время')
            return handler_result(new_rings, answer)
        rings.append(Ring(start=start, end=end))
    await Ring.filter(deleted__isnull=True).update(deleted=datetime.now())
    await Ring.bulk_create(rings)
    await msg.reply(answer := 'Создано расписание звонков')
    answer += str(await rings_handler(msg, ctx))
    return handler_result(new_rings, answer)