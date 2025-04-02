# Модуль с обработчиком информации

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .tools import handler_result
from .types import Context, Filter
from .tools import schedule, rings, info, weather, holidays, subscribe
from .tools import (
    cmd_reset_student_class_schedule,
    cmd_new_weekends, 
    cmd_new_rings, 
    cmd_new_holidays, 
    cmd_menu, 
    cmd_start,
    cmd_mailing,
    cmd_mailing_teachers,
    cmd_mailing_student_classes,
    cmd_teacher,
    cmd_teacher_subscribe,
    cmd_teachet_unsubscribe,
    cmd_reset_teacher_schedule,
)
from modules import b, pre
from config import BOT_ADMINS
    
@dispatcher.message(Filter(text=info))
async def info_handler(msg: Message, ctx: Context):
    await msg.reply(answer := 
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
    from loguru import logger
    logger.info({'id': ctx.user.id, 'admins': BOT_ADMINS})
    if ctx.user.id in BOT_ADMINS:
        text = (
            b('Команды админа (видит только админы):\n')
            +f'- {b(cmd_new_rings)} - Обновить раписание звонков '
            +f'(на каждой строке время начала и время окончания, например {pre("08:20-09:00")})\n'
            +f'- {b(cmd_new_holidays)} - Обновить расписание каникул '
            +f'(на каждой строке описание даты, например {pre("28 октября (пн) - 02 ноября (сб)")})\n'
            +f'- {b(cmd_new_weekends)} - Обновить раписание выходных '
            +f'(на каждой строке описание даты {pre("4 ноября (пн)")})\n'
            +f'- {b(cmd_reset_student_class_schedule)} - Сбросить классы, расписание и подписки\n'
            +f'- {b(cmd_reset_teacher_schedule)} - Сбросить учителей, расписание и подписки\n'
            +f'- {b(cmd_mailing)} - Рассылка сообщения всем пользователям\n'
            +f'- {b(cmd_mailing_teachers)} - Рассылка всем подписанным на учителей\n'
            +f'- {b(cmd_mailing_student_classes)} - Рассылка всем подписанным на расписание классов\n'
            +b('\nСкрытые команды (могут использовать все):\n')
            +f'- {b(cmd_teacher)} ФАМИЛИЯ ДЕНЬ_НЕДЕЛИ - получить расписание учителя. '
            +'Если не введен день недели, то будет показано расписание на всю неделю\n'
            +f'- {b(cmd_teacher_subscribe)} ФАМИЛИЯ - подписаться на рассылку расписания учителя\n'
            +f'- {b(cmd_teachet_unsubscribe)} ФАМИЛИЯ - отписаться от рассылки на расписание учителя\n'
        )
        answer += text
        await msg.reply(text)
    return handler_result(info_handler, answer)
    