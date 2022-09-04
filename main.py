# получаем токен сервиса openweather и импортируем в main
import requests
import datetime
from pprint import pprint
from config import open_weather_token


# составляем и делаем гет запрос к API openweather, чтоб получить данные погоды

def get_weather(city, open_weather_token):
    try:
        # из документации на сайте openweather копируем ссылку для осуществления гет запроса по имени города
        r = requests.get(
          f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = int((data["main"]["pressure"])/1.333)
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        print(f"Погода в городе: {city}\nТемпература: {cur_weather}С\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
              f"Скорость ветра: {wind} м/с\nВосход: {sunrise_timestamp}\n"
              f"Закат: {sunset_timestamp}")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")



def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)


if __name__ == '__main__' :
    main()
