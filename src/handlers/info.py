# Модуль с обработчиком информации

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import get_filter, handler_result
from .types import Context
from .tools import schedule, rings, info, weather, holidays, subscribe
from .tools import cmd_new_weekends, cmd_new_rings, cmd_new_holidays, cmd_menu, cmd_start
from modules import b
from config import BOT_ADMINS
    
@dispatcher.message(get_filter(text=info))
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
        f'- {b(cmd_start)} - Начать работу с ботом\n'
        f'- {b(cmd_menu)} - Перейти в меню\n'
        f'- {b("КлассБуква ДеньНедели")} (10а вторник) - '
        'Узнать расписание сразу на нужный класс и день (всю неделю)')
    if ctx.user.id in BOT_ADMINS:
        text = (
            b('Команды админа (видит только админы):\n')
            +f'- {b(cmd_new_rings)} - Обновить раписание звонков\n'
            +f'- {b(cmd_new_holidays)} - Обновить расписание каникул\n'
            +f'- {b(cmd_new_weekends)} - Обновить раписание выходных\n'
        )
        answer += text
        await msg.answer(text)
    return handler_result(info_handler, answer)
    