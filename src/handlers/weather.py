# Модуль с обработчиком погоды

# Встроенные модули
from math import floor
from datetime import date

# Внешние модули
from aiogram.types import Message

# Внутренние модули
from dispatcher import dispatcher
from .types import Context, Filter
from .tools import handler_result, weather
from modules import WeatherAPI, b, WeatherEnum
from config import WEATHER_API_KEY

weather_api = WeatherAPI(WEATHER_API_KEY, 56.875299, 53.219367)
    
@dispatcher.message(Filter(text=weather))
async def weather_handler(msg: Message, ctx: Context):
    weather_result = await weather_api.fetch()
    month = date.today().month
    if month in [1, 2, 3, 12]:
        if weather_result.temperature >= -15:
            answer = b('Похоже, что на улице зима')
        else:
            answer = b('В такой мороз лучше не гулять')
    else:
        answer = {
            WeatherEnum.RAIN: b('На улице дождь\nОднозначно не улица'),
            WeatherEnum.CLOUDS: b('На улице облачно.\nДумаю, что скоро может нагрянуть дождь'),
            WeatherEnum.CLEAR: b('Небо чисто\nПочему бы и не погулять?'),
            WeatherEnum.PARTY_CLOUD: b('Немного облачно\nПочему бы и не погулять?'),
        }.get(weather_result.weather, b('Даже не знаю, что за погода'))
    answer += f'\nНа улице {b(floor(weather_result.temperature))}°C'
    await msg.reply(answer)
    return handler_result(weather_handler, answer)
    