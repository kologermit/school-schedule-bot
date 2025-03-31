# Модуль с обработчиком меню

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import handler_result
from .tools import get_filter
from .tools import schedule, subscribe, menu, rings, holidays
from .types import Context
from .screens import menu_buttons, menu_screen, to_menu
from .screens import to_schedule
from .screens import to_subscribe
from .rings import rings_handler
from .holidays import holidays_handler
    
async def info_handler(msg: Message, ctx: Context):
    await msg.answer(answer := 
        'Кнопки для пользования ботом:\n'
        '1. Уроки - Узнать расписание уроков\n'
        '2. Звонки - Узнать расписание звонков\n'
        '3. Информация - Узнать подробную информацию о боте\n'
        '4. Где физ-ра? - Узнать, где будет физ-ра - на улице или в зале.\n\n'
        'Команды:\n'
        '1. /start - Начать работу с ботом\n'
        '2. /restart - Перезапустить бота\n'
        '3. /info - Узнать подробную информацию о боте\n'
        '4. КлассБуква ДеньНедели (10а вторник) - Узнать расписание сразу на нужный класс и день (всю неделю)')
    return answer
    