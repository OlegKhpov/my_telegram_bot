import requests

CITY_ID = 'CITY_CODE'  # Insert your code
OPEN_WEATHER_API_KEY = 'API_KEY'  # Insert your api key from openweathermap.org
WEATHER = {
    '200': "thunderstorms",
    '300': 'drizzle',
    '500': 'rain',
    '600': 'snow',
    '700': 'atmosphere',
    '800': 'clear',
    '801': 'clouds'
}


def get_weather_now(city=CITY_ID):
    URL = 'http://api.openweathermap.org/data/2.5/weather'
    response = requests.get(URL, params={
        'id': city,
        'appid': OPEN_WEATHER_API_KEY,
        'lang': 'ru',
        'units': 'metric',
    })
    response = response.json()
    description = response.get('weather')[0].get('description').capitalize()
    temp = response.get('main').get('temp')
    temp_max = response.get('main').get('temp_max')
    temp_min = response.get('main').get('temp_min')
    pressure = response.get('main').get('pressure')
    wind_speed = response.get('wind').get('speed')
    wind_dir = response.get('wind').get('deg')
    return f'Погода в Измаиле:\
        \n"{description}"\
        \nТемпература: {temp}°\
        \nМаксимально: {temp_max}°, Минимально: {temp_min}°\
        \nДавление: {pressure} мм \
        \nВетер: {wind_speed}, направление: {wind_dir}'
