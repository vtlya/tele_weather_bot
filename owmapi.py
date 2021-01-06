import requests

def weather_now(city,apikey):
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + str(city) + '&APPID='+apikey+'&units=metric&lang=ru')
        weather = dict(list(r.json()["weather"])[0])["description"]  # просто общие сведения о том какая погода
        temp_now = dict(r.json()["main"])["temp"]  # температура сейчас в цельсиях
        temp_min = dict(r.json()["main"])["temp_min"]  # минимальная температура сейчас
        feels_like = dict(r.json()["main"])["feels_like"]  # как ощущается температура в цельсиях
        pressure = dict(r.json()["main"])["pressure"]  # какое давление сейчас кПа
        humidity = dict(r.json()["main"])["humidity"]  # какая влажность сейчас в %
        try:
            wind_speed = dict(r.json()["wind"])["speed"]  # скорость ветра в мс
            wind_deg = dict(r.json()["wind"])["deg"]  # направление ветра от севера по часовой стрелки
            clouds = dict(r.json()["clouds"])["all"]  # покрытие облаками в %
        except:
            wind_speed = '?' # скорость ветра в мс
            wind_deg = '?'  # направление ветра от севера по часовой стрелки
            clouds = '?'  # покрытие облаками в %

        def wind_side(wind_deg):  # возвращает сторону света с которой дует ветер
            try:
                if (wind_deg > 337 and wind_deg <= 360) or (wind_deg > 0 and wind_deg <= 23):
                    return "C"
                elif wind_deg > 23 and wind_deg <= 67:
                    return "CВ"
                elif wind_deg > 67 and wind_deg <= 113:
                    return "В"
                elif wind_deg > 113 and wind_deg <= 157:
                    return "ЮВ"
                elif wind_deg > 157 and wind_deg <= 203:
                    return "Ю"
                elif wind_deg > 203 and wind_deg <= 247:
                    return "ЮЗ"
                elif wind_deg > 247 and wind_deg <= 293:
                    return "З"
                elif wind_deg > 293 and wind_deg <= 337:
                    return "СЗ"
                else:
                    return "непонятно какой:)"
            except:
                return "непонятно какой:)"

        def precipitation(json):
            try:
                try:
                    rain = 'За последние 3 часа выпало *' + str(dict(json["rain"])["3h"]) + ' мм* осадков\n'
                except:
                    rain = 'За последний час выпало *' + str(dict(json["rain"])["1h"]) + ' мм* осадков\n'
            except:
                rain = ''
            try:
                try:
                    snow = 'За последние 3 часа выпало *' + str(dict(json["snow"])["3h"]) + ' мм* осадков\n'
                except:
                    snow = 'За последний час выпало *' + str(dict(json["snow"])["1h"]) + ' мм* снега\n'
            except:
                snow = ''
            return str(rain) + '' + str(snow)

        return '🌈☀️🌤⛅️🌥☁️🌦🌧⛈🌩🌨❄️'+\
        '\nВ городе _' + str(city) + '_ сейчас *' + str(weather) + '*.\nТемпература воздуха: *' + str(
        temp_now) + '℃* \n(min: ' + str(temp_min) +'℃), которая ощущается как *' + str(feels_like) + '℃*,'  \
           + '\nТекущее давление: _' + str(round(pressure * 100 / 133)) + ' мм р.ст._' \
           + '\nВлажность воздуха составляет: _' + str(humidity) + '%_' \
           + '\nВетер *' + wind_side(wind_deg) + '* и составляет *' + str(wind_speed) + ' м/с*.' \
           + '\nПокрытие облаками составляет *' + str(clouds) + '%*\n' \
           + precipitation(r.json())
    except:
        return ''

# метод для получения текста с погодой для форкаста на сегодня - пока не реализован :(
def weather_forecast_today(city,apikey):
    pass

# метод для получения текста с погодой для форкаста на завтра - пока не реализован :(
def weather_forecast_tomorrow(city,apikey):
    pass




