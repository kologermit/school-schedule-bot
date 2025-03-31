# Модуль с обработчиком информации

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from .types import Context
from .tools import schedule, rings, info, weather
from modules import b
    
async def info_handler(msg: Message, ctx: Context):
    await msg.answer(answer := 
        f'{b("Кнопки для пользования ботом:")}\n'
        f'{b("1.")} {b(schedule)} - Узнать расписание уроков\n'
        f'{b("2.")} {b(rings)} - Узнать расписание звонков\n'
        f'{b("3.")} {b(info)} - Узнать подробную информацию о боте\n'
        f'{b("4.")} {b(weather)} - Узнать, где будет физ-ра - на улице или в зале.\n\n'
        f'{b("Команды:")}\n'
        f'{b("1.")} /start - Начать работу с ботом\n'
        f'{b("2.")} /restart - Перезапустить бота\n'
        f'{b("3.")} /info - Узнать подробную информацию о боте\n'
        f'{b("4.")} КлассБуква ДеньНедели (10а вторник) - '
        'Узнать расписание сразу на нужный класс и день (всю неделю)')
    return answer
    