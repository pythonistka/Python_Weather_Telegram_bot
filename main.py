# получаем токен сервиса openweather и импортируем в main
import requests
import datetime
from pprint import pprint
from config import open_weather_token


# составляем и делаем гет запрос к API openweather, чтоб получить данные погоды


def get_weather(city, open_weather_token):
    # создаем словарь о состоянии погоды + эмоджи

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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

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

        print(f"****{datetime.datetime.now().strftime('%Y-%m-%d %H-%M')}****\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}°С {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
              f"Скорость ветра: {wind} м/с\nВосход: {sunrise_timestamp}\n"
              f"Закат: {sunset_timestamp}\n"
              f"Продолжительность светового дня: {lenght_of_the_day}\n"
              f"Хорошего дня!")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
