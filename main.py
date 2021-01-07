import telebot
import json
from telebot import types
import os

telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(telegram_token) # key от бота

global json_path
json_path ='times.json' # путь к json-бд
global user_list
user_list = 'users.json' # пользователи бота пишутся сюда

print('main.py raned')

@bot.message_handler(commands=['start']) # хендлер для команды старт
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.chat.first_name + '! Я бот который будет присылать тебе уведомления о погоде на текущий день и завтра в оговоренное время. я пока нахожусь в разработке правда')
    #print('get start command and send gretting message') #лог для отладки
    write_user(message.from_user.username, message.chat.id)
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('London')
    itembtnv = types.KeyboardButton('Moscow')
    itembtnc = types.KeyboardButton('Omsk')
    itembtnd = types.KeyboardButton('Sochi')
    itembtne = types.KeyboardButton('Vladivostok')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd, itembtne)
    bot.send_message(message.chat.id, "Выбери город", reply_markup=markup)
    #print('send messge with city') #лог для отладки

@bot.message_handler(content_types=['text']) # хендлер для всех текстов
def send_text(message):
    global city
    global id_and_city
    if message.text in ['London', 'Moscow', 'Omsk', 'Sochi', 'Vladivostok']:
        city = message.text
        bot.send_message(message.chat.id, 'Ты выбрал город ' + message.text + '.')
        markup = types.ReplyKeyboardMarkup()
        item8 = types.KeyboardButton('8:00')
        itemb9 = types.KeyboardButton('9:00')
        item12 = types.KeyboardButton('12:00')
        item16 = types.KeyboardButton('16:00')
        item20 = types.KeyboardButton('20:00')
        itemall = types.KeyboardButton('Во все времена')
        itemothercity = types.KeyboardButton('/start выбрать другой город')
        markup.row(item8, itemb9, item12, item16, item20)
        markup.row(itemall)
        markup.row(itemothercity)
        bot.send_message(message.chat.id, "Теперь выбери во сколько ты желаешь получать уведомления о погоде", reply_markup=markup)
        #print('send messge with time') #лог для отладки
    elif message.text in ['8:00', '9:00', '12:00', '16:00', '20:00', 'Во все времена']:
        if message.text in ['8:00', '9:00', '12:00', '16:00', '20:00']:
            markup = types.ReplyKeyboardMarkup().row(types.KeyboardButton('/start выбрать другой город и время'))
            write_json(message.text, message.chat.id, city)
            bot.send_message(message.chat.id, 'Буду отправлять тебе погоду в ' + message.text +' часов каждый день, для города '+city+'!', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup().row(types.KeyboardButton('/start выбрать другой город и время'))
            write_manytime_json(['8:00', '9:00', '12:00', '16:00', '20:00'], message.chat.id, city)
            bot.send_message(message.chat.id, 'Буду отправлять тебе погоду в 8:00, 9:00, 12:00, 16:00 и 20:00 часов каждый день, для города '+city+'!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Ты выбрал недопустимый город или время, нажми на нужную кнопку внизу под клавиатурой.\nИли напиши /start , чтобы начать работать с ботом с нуля.\n_P.S. Я не отвечаю на билеберду!_', parse_mode='Markdown')
        #print('wrong message from user') #лог для отладки

# метод записывает в json подписчиков на данное время и город
def write_json(time, chat_id, city):
    with open(json_path) as f:
        file_content = f.read()
        data = json.loads(file_content)
    try:
        a = list(data[time][city])
        a.append(chat_id)
        data[time].__setitem__(city, list(set(a)))
        #print('succesfull subscribe at '+ str(time) + ', city:' + str(city)) #лог для отладки
    except:
        data[time].__setitem__(city,list([]))
        a = list(data[time][city])
        a.append(chat_id)
        data[time].__setitem__(city, list(set(a)))
        #print('succesfull subscribe at '+ str(time) + ', city:' + str(city)) #лог для отладки
    with open(json_path, 'w') as f:
        f.write(json.dumps(data))
        print('one time notification created. chat_id:' + str(chat_id)) #лог для отладки

# метод записывает в json подписчиков на все времена и город
def write_manytime_json(time, chat_id, city):
    with open(json_path) as f:
        file_content = f.read()
        data = json.loads(file_content)
    for i in time:
        try:
            a = list(data[i][city])
            a.append(chat_id)
            data[i].__setitem__(city, list(set(a)))
            #print('succesfull subscribe at '+ str(i) + ', city:' + str(city)) #лог для отладки
        except:
            data[i].__setitem__(city, list([]))
            a = list(data[i][city])
            a.append(chat_id)
            data[i].__setitem__(city, list(set(a)))
            #print('succesfull subscribe at '+ str(i) + ', city:' + str(city)) #лог для отладки
    print(data)
    with open(json_path, 'w') as f:
        f.write(json.dumps(data))
        print('many times notifications created. chat_id:' + str(chat_id)) #лог для отладки

def write_user(username, chat_id):
    with open(user_list) as f:
        file_content = f.read()
        data = json.loads(file_content)
    try:
        data.__setitem__(username, chat_id)
    except:
        pass
    with open(user_list, 'w') as f:
        f.write(json.dumps(data))
        print('+ 1 user:"' + str(username) + '", with chat:' + str(chat_id)) #лог для отладки

# метод удаляет все подписки у пользователя - пока не реализован :(
def delete_supscriptions(chat_id):
    pass

bot.polling()