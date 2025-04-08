
from datetime import datetime, timedelta
from copy import deepcopy

from aiogram.types import Message as TGMessage

from dispatcher import dispatcher, bot_async
from .types import Context, Filter
from .tools import handler_result, mailing
from .tools import cmd_mailing, cmd_mailing_student_classes, cmd_mailing_teachers, cmd_stats
from models import StudentClassSubscribe, User, TeacherSubscribe, Teacher, StudentClass, Message
from modules import b
from config import BOT_ADMINS


@dispatcher.message(Filter(admin=True, 
    pattern=f'^({cmd_mailing}).*'))
async def mailing_handler(msg: TGMessage, ctx: Context):
    text = deepcopy(ctx.message.text)
    text = text.replace(cmd_mailing_teachers, '').strip()
    text = text.replace(cmd_mailing_student_classes, '').strip()
    text = text.replace(cmd_mailing, '').strip()
    if not text:
        await msg.reply(answer := b('Нет сообщения для рассылки!'))
        return handler_result(mailing_handler, answer)
    if cmd_mailing_teachers in ctx.message.text:
        text = b('Рассылка учителям:\n\n') + text
        user_ids = await TeacherSubscribe.filter_all().values_list('user_id', flat=True)
    elif cmd_mailing_student_classes in ctx.message.text:
        text = b('Рассылка ученикам:\n\n') + text
        user_ids = await StudentClassSubscribe.filter_all().values_list('user_id', flat=True)
    else:
        text = b('Общая рассылка:\n\n') + text
        user_ids = await User.filter().values_list('id', flat=True)
    await mailing(text, user_ids, bot_async)
    await msg.reply(answer := b(f'Отправлено сообщений: {len(user_ids)}'))
    return handler_result(mailing_handler, answer)

@dispatcher.message(Filter(admin=True, text=cmd_stats))
async def stats(msg: TGMessage, ctx: Context):
    now = datetime.now()
    await msg.reply(answer := '\n'.join(f'{b(key)}: {value}' for key, value in {
        'Админ': f'{ctx.user.name} ({ctx.user.id})', 
        'Пользователей': await User.all().count(),
        'Классов': await StudentClass.filter_all().count(),
        'Учителей': await Teacher.filter_all().count(),
        'Подписок учителей': await TeacherSubscribe.filter_all().count(),
        'Подписок классов': await StudentClassSubscribe.filter_all().count(),
        'Сообщений за 24ч': await Message.filter(created__gte=now-timedelta(days=1)).count(),
        'Сообщений за 7 дней': await Message.filter(created__gte=now-timedelta(days=7)).count(),
        'Сообщений за 30 дней': await Message.filter(created__gte=now-timedelta(days=30)).count(),
        'Админы': '\n'.join(f'{b(u.id)}: {u.name}' for u in await User.filter(id__in=BOT_ADMINS)),
    }.items()))
    return handler_result(stats, answer)
