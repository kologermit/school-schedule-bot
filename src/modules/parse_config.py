# Модуль сбора настроек 

# Встроенные модули
from os import getenv
from sys import argv, stderr
from copy import deepcopy
from json import load, loads

# Внешние модули
from dotenv import load_dotenv

# Вынес повторяются строки в отдельные переменные
summary = 'summary'
default='default'
required='required'
json='json'
project_summary='project_summary'

# Функция парсинга конфига и формирования кода
def parse_config_to_exec(args: dict[str, str]) -> str:
    # Вынес повторяющиеся строки в переменные
    env_file='env_file'
    # Вывод справки при добавлении параметра -h
    if set((help_args := ['-h', '--help', 'help'])) & set(argv):
        print(args[project_summary])
        print()
        print(f'{", ".join(help_args)} Справка по использованию')
        print()
        print(f'--{env_file}=env.json Файл с переменными')
        for arg, data in args.items():
            if arg == project_summary: continue
            print(f'\n--{arg}=text {data[summary]}')
        exit()

    # Функция для поиска аргумента
    def parse_argv(key_arg: str, default: str | None =None) -> str | None:
        find_key = '--'+key_arg+'='
        for arg in argv:
            if arg.startswith(find_key):
                return arg[len(find_key):]
        return default

    # Загрузка конфига из файла, если таковой указан
    env_file_data = {}
    if (env_file := parse_argv(env_file)) is not None:
        env_file_data = load(open(env_file))

    load_dotenv()
    result = []

    # Парсинг конфига
    # Приоритет аргументов (последние в приоритете):
    # - Значение по умолчанию (default)
    # - Значение из переменных окружения и .env файла
    # - Значение из файла конфигурации (env_file)
    # - Значение из агрументов командной строки
    for arg in deepcopy(args):
        if arg == project_summary: continue
        data = deepcopy(args[arg])
        # Наименьший приоритет у переменной окружения
        env_arg = getenv(arg, data.get(default, None))
        # Следующий приоритет у переданного файла конфига
        env_file_arg = env_file_data.get(arg, env_arg)
        # Высший приоритет у аргумента из консоли
        args[arg] = parse_argv(arg, env_file_arg)
        if data.get(json, False):
            args[arg] = loads(args[arg])

        if args[arg] == '':
            args[arg] = None

        if data.get(required, False) and args[arg] is None:
            print(f'Обязательный аргумент {arg} не найден!', file=stderr)
            exit(1)
        # Перенос каждой переменной в вид константы
        # Чтобы можно было импортировать, как from config import LOG_DIR
        result.append(f'{arg}={args[arg].__repr__()}')
        
    # Возвращение результата
    return '\n'.join(result)