# Модуль работы с кнопками

# Встроенные модули
from copy import deepcopy

# Внешние модули
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup

cmd_start = '/start'
back = 'Назад🔙'
menu = 'Меню'
cmd_menu = '/menu'
schedule = 'Уроки📅'
cmd_reset_student_class_schedule = '/reset_student_class_schedule'
cmd_reset_teacher_schedule = '/reset_teacher_schedule'
cmd_mailing = '/mailing'
cmd_mailing_teachers = '/mailing_teachers'
cmd_mailing_student_classes = '/mailing_student_classes'
cmd_stats='/stats'
rings = 'Звонки🔔'
cmd_new_rings = '/new_rings'
holidays = 'Каникулы🎅'
cmd_new_holidays = '/new_holidays'
cmd_new_weekends = '/new_weekends'
info = 'Информацияℹ'
add = 'Добавить🆕'
delete = 'Удалить❌'
weather = 'Погода☂️'
subscribe = 'Рассылка расписания📩'
cmd_teacher = '/t'
cmd_teacher_subscribe = '/ts'
cmd_teachet_unsubscribe = '/tu'


def list_to_keyboard(btns: list[list[str]]):
    btns.append([menu])
    for i, list_btns in enumerate(deepcopy(btns)):
        for j, btn in enumerate(list_btns):
            btns[i][j] = KeyboardButton(text=btn)
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

def list_to_inline_keiboard(btns: list[dict[str, str]]):
    for i, dict_btns in enumerate(deepcopy(btns)):
        btns[i] = [IButton(text=text, callback_data=data) 
            for text, data in dict_btns.items()]
    return IMarkup(inline_keyboard=btns)