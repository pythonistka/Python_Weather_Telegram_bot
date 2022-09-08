import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


# оборачиваем функцию в декоратор massege.handler
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и пришлю тебе сводку погоды ;)")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        # из документации на сайте openweather копируем ссылку для осуществления гет запроса по имени города
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = int(data["main"]["temp"])

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, брат"

        humidity = data["main"]["humidity"]
        pressure = int((data["main"]["pressure"]) / 1.333)
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"****{datetime.datetime.now().strftime('%Y-%m-%d %H-%M')}****\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}°С {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
                            f"Скорость ветра: {wind} м/с\nВосход: {sunrise_timestamp}\n"
                            f"Закат: {sunset_timestamp}\n"
                            f"Продолжительность светового дня: {lenght_of_the_day}\n"
                            f"***Хорошего дня!***")

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
