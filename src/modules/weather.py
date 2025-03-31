# Модуль запросов в OpenWeatherApi

# Встроенные модули
from copy import deepcopy

# Внешние модули
from aiohttp import ClientSession

class WeatherEnum:
    RAIN = 'Rain'
    CLOUDS = 'Clouds'
    CLEAR = 'Clear'
    PARTY_CLOUD = 'Party Cloud'
        
class Weather:
    weater: str
    temperature: float
    def __init__(self, weather: str, temperature: float):
        self.weater = deepcopy(weather)
        self.temperature = deepcopy(temperature)

class WeatherAPI:
    api_key: str
    lat: float
    lon: float
    def __init__(self, api_key: str, lat: float, lon: float):
        self.api_key = deepcopy(api_key)
        self.lat = deepcopy(lat)
        self.lon = deepcopy(lon)
            
    async def fetch(self) -> Weather:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "ru"
        }

        async with ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data["cod"] == 200:
                        return Weather(
                            weather=data["weather"][0]["main"],
                            temperature=data["main"]["temp"],
                        )
                    else:
                        raise ValueError(f'Ошибка API: {data["message"]}')
                else:
                    raise ValueError(f'Ошибка HTTP: {response.status}')