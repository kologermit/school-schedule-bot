# Модуль конфига сервиса

# Внутренние модули
from modules.parse_config import parse_config_to_exec
from modules.parse_config import json, required, summary, default, project_summary

PROJECT_NAME = 'school-schedule-bot'
PROJECT_SUMMARY = 'Бот со школьным расписанием'

LOGS_DIR='LOGS_DIR'
TMP_DIR='TMP_DIR'
DB_HOST='DB_HOST'
DB_PORT='DB_PORT'
DB_NAME='DB_NAME'
DB_USER='DB_USER'
DB_PASSWORD='DB_PASSWORD'
WEATHER_API_KEY='WEATHER_API_KEY'
BOT_TOKEN='BOT_TOKEN'
BOT_START_MESSAGE='BOT_START_MESSAGE'
BOT_ADMINS='BOT_ADMINS'

exec(parse_config_to_exec({
    project_summary: PROJECT_SUMMARY,
    LOGS_DIR: {summary: 'Путь к папке с логами. \n'
        'Если значение не задано, то лог не будет выводиться в файлы. \n'
        'По умолчанию ""', default: ''},
    TMP_DIR: {summary: 'Папка для веременных файлов. Обязательный параметр', required: True},
    DB_HOST: {summary: 'Хост БД Postgres. По умолчанию localhost', default: 'localhost'},
    DB_PORT: {summary: 'Порт БД Postgres. По умолчанию 5432', default: '5432'},
    DB_USER: {summary: 'Имя пользователя БД. По муолчанию postgres', default: 'postgres'},
    DB_PASSWORD: {summary: 'Пароль БД Postgres. По умолчанию qwerty', default: 'qwerty'},
    WEATHER_API_KEY: {summary: 'API ключ к сервису OpenWeatherAPI. Обязательный параметр', 
        required: True},
    DB_NAME: {summary: 'Имя БД Postgres. По умолчанию bot', default: 'bot'},
    BOT_TOKEN: {summary: 'Токен для доступа к АПИ бота. Обязательный параметр', required: True},
    BOT_START_MESSAGE: {summary: 'Стартовое сообщение, которое рассылается всем админам при запуске. \n'
        'По умолчанию "Запуск сервиса servicename"', default: 'Запуск сервиса '+PROJECT_NAME},
    BOT_ADMINS: {summary: 'IDs админов бота. '
        'Первому в списке будет приходить уведомления о запуске бота и об ошибках. '
        'По умолчанию []', default: '[]', json: True}
}))