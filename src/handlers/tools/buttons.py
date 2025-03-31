# Модуль работы с кнопками

# Встроенные модули
from copy import deepcopy

# Внешние модули
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup

back = 'Назад🔙'
menu = 'Меню'
schedule = 'Уроки📅'
rings = 'Звонки🔔'
holidays = 'Каникулы🎅'
info = 'Информацияℹ'
add = 'Добавить🆕'
delete = 'Удалить❌'
weather = 'Погода☂️'
subscribe = 'Рассылка расписания📩'


def list_to_keyboard(btns: list[list[str]]):
    for i, list_btns in enumerate(deepcopy(btns)):
        for j, btn in enumerate(list_btns):
            btns[i][j] = KeyboardButton(text=btn)
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

def list_to_inline_keiboard(btns: list[dict[str, str]]):
    for i, dict_btns in enumerate(deepcopy(btns)):
        btns[i] = [IButton(text=text, callback_data=data) 
            for text, data in dict_btns.items()]
    return IMarkup(inline_keyboard=btns)