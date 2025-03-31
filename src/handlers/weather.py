# Модуль с обработчиком погоды

# Встроенные модули
from math import floor
from datetime import date

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from .types import Context
from modules import WeatherAPI, b, WeatherEnum
from config import WEATHER_API_KEY

weather_api = WeatherAPI(WEATHER_API_KEY, 56.875299, 53.219367)
    
async def weather_handler(msg: Message, ctx: Context):
    weather = await weather_api.fetch()
    month = date.today().month
    if month in [1, 2, 3, 12]:
        if weather.temperature >= -15:
            answer = b('Похоже, что на улице зима')
        else:
            answer = b('В такой мороз лучше не гулять')
    else:
        answer = {
            WeatherEnum.RAIN: b('На улице дождь\nОднозначно не улица'),
            WeatherEnum.CLOUDS: b('На улице облачно.\nДумаю, что скоро может нагрянуть дождь'),
            WeatherEnum.CLEAR: b('Небо чисто\nПочему бы и не погулять?'),
            WeatherEnum.PARTY_CLOUD: b('Немного облачно\nПочему бы и не погулять?'),
        }.get(weather.weater, b('Даже не знаю, что за погода на улице, но за окном'))
    answer += f'\nНа улице {b(floor(weather.temperature))}°C'
    await msg.answer(answer)
    return answer
    