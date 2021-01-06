import telebot
import json
import schedule
import time
from owmapi import weather_now
import os

global json_path
json_path = 'times.json'  # путь к json-бд

telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(telegram_token) # key от бота

apikey = os.environ['OWM_API_KEY']  # open weather map api key

print('sheduler.py raned')

# метод вскрывает json и делает отправку всем подписчикам погоды на данное время
def msg(apikey, time):
    # когда наступило заданное время открываем json
    with open(json_path) as f:
        data = json.load(f)
    try:
        for city in data[time]:  # перебираем города для данного времени
            try:
                weather = str(weather_now(city, apikey))  # узнаем погоду для этого города в данный момент
                print('succesful got weather for city:' + city + ', at time:'+time)
                if weather == '':
                    weather = 'Блин:( Что-то не получилось получить погоду для _'+ city +'_ в данное время. Сори('
            except:
                weather = 'Блин:( Что-то не получилось получить погоду для _'+ city +'_ в данное время. Сори('

            # forecast # в owmapi добавить методы для форкастов, чтобы также их прысылать. на +3 часа сегодня и на завтра

            try:
                users = list(data[time][city])  # дублируем массив юзеров для данного города и времени
            except:
                users = []
            for user in users:
                print('Пошла команда: bot.send_message(' + str(user) + ', weather, parse_mode="Markdown")') #какая функция сработала
                try:
                    bot.send_message(user, weather, parse_mode='Markdown')  # делаем рассылку погоды каждому
                    print(time +', succesful message to user:'+user+', for city:'+ city)
                except:
                    bot.send_message(user, weather, parse_mode='Markdown')  # делаем рассылку погоды каждому
                    print('Не отправилось письмо! Что-то с телеграм либой походу :(')
                bot.send_message(user, weather, parse_mode='Markdown')  # делаем рассылку погоды каждому
    except:
        pass

#шедулим отправку для времен с двузначным значением
times2 = ["10:00", "11:00", "12:00", "13:00",
          "15:45",
          "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00"]
for hour in times2:
    schedule.every().day.at(str(hour)).do(msg, apikey, hour)
    print('sheduled at '+ hour)

#шедклим отправку для времен с однозначным значением
times1 = [ "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00"]
for hour in times1:
    h2 = '0'+str(hour)
    schedule.every().day.at(str(h2)).do(msg, apikey, hour)
    print('sheduled at ' + hour)

while True:
    schedule.run_pending()
    time.sleep(20)
