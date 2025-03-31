# Модуль с обработчиком информации

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from .types import Context
from .tools import schedule, rings, info, weather, holidays, subscribe
from modules import b
    
async def info_handler(msg: Message, ctx: Context):
    await msg.answer(answer := 
        f'{b("Кнопки для пользования ботом:")}\n'
        f'- {b(schedule)} - Узнать расписание уроков\n'
        f'- {b(rings)} - Узнать расписание звонков\n'
        f'- {b(holidays)} - Узнать расписание каникул\n'
        f'- {b(info)} - Узнать подробную информацию о боте\n'
        f'- {b(weather)} - Узнать, где будет физ-ра - на улице или в зале.\n'
        f'- {b(subscribe)} - Подписаться на рассылку расписания\n'
        f'\n{b("Команды:")}\n'
        f'- {b("/start")} - Начать работу с ботом\n'
        f'- {b("/menu")} - Перейти в меню\n'
        f'- {b("КлассБуква ДеньНедели")} (10а вторник) - '
        'Узнать расписание сразу на нужный класс и день (всю неделю)')
    return answer
    