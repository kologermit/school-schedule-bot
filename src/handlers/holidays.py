# Модуль с обработчиком праздников

# Встроенные модули
from datetime import time, datetime

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import get_filter, handler_result
from .tools import cmd_new_holidays, cmd_new_weekends, holidays
from models import Holiday
from modules import b
from .types import Context
    
@dispatcher.message(get_filter(text=holidays))
async def holidays_handler(msg: Message, ctx: Context):
    holidays = await Holiday.filter(deleted__isnull=True, is_holiday=True).order_by('id')
    weekends = await Holiday.filter(deleted__isnull=True, is_weekend=True).order_by('id')
    answer = (b('Каникулы:\n')
        +'\n'.join(f'{b(i+1)}. {holiday.summary}' for i, holiday in enumerate(holidays))
        +'\n\n'+b('Выходные:\n')
        +'\n'.join(f'{b(i+1)}. {holiday.summary}' for i, holiday in enumerate(weekends))
    )
    await msg.answer(answer)
    return handler_result(holidays_handler, answer)


# /new_holidays или /new_weekends
# Праздники1
# Праздники2
# ...
@dispatcher.message(get_filter(pattern=f'^({cmd_new_holidays}|{cmd_new_weekends}).*', admin=True))
async def new_holidays(msg: Message, ctx: Context):
    split = ctx.message.text.split('\n')
    is_holidays = cmd_new_holidays in split[0]
    await Holiday.filter(is_holiday=is_holidays, deleted__isnull=True).update(deleted=datetime.now())
    await Holiday.bulk_create(
        map(lambda line: Holiday(
            summary=line, 
            is_holiday=is_holidays,
        ), split[1:]))
    await msg.answer(answer := 'Каникулы обновлены')
    answer += await holidays_handler(msg, ctx)
    return handler_result(new_holidays, answer)