import telebot
import config
import parser_Y_W as weather
import json as js

data = {}
id = 0
def start():
    global data
    file = open('data.js', 'r')
    data = js.load(file)
    file.close()
start()

def update_data():
    global data
    file = open('data.js', 'w')
    data = js.dump(data, file)
    file.close()

def get_help():
    return str(''.join(list(map(lambda x: x + ' - ' + config.HELP.get(x) + '\n' , config.HELP.keys()))))

def get_stat():
    start()
    global data
    return str(''.join(list(map(lambda x: x + ': ' + data.get(x) + '\n' , data.keys()))))

bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands = ['start', 'help'])
def help(message):
    global id
    id = 0
    bot.send_message(message.chat.id, get_help())

@bot.message_handler(commands = ['set_time'])
def sett(message):
    global id
    id = 1
    bot.send_message(message.chat.id, "Введите время в 24-часовом формате")

@bot.message_handler(commands = ['set_town'])
def sett(message):
    global id
    id = 2
    bot.send_message(message.chat.id, "Введите название города")

@bot.message_handler(commands = ['status'])
def stat(message):
    bot.send_message(message.chat.id, get_stat())

@bot.message_handler(commands = ['weather'])
def stat(message):
    bot.send_message(message.chat.id, weather.get(data['TOWN']))

@bot.message_handler(content_types = 'text')
def set(message):
    global id
    if (id == 1):
        data['TIME'] = message.text
        bot.send_message(message.chat.id, "Время изменено на " + data['TIME'])
        update_data()
    elif (id == 2):
        data['TOWN'] = message.text
        bot.send_message(message.chat.id, "Город изменен на " + data['TOWN'])
        update_data()
    elif (id == 0):
        bot.send_message(message.chat.id, "Не понимаю команды")
    else: bot.send_message(message.chat.id, "Ошибка")
    id = 0

#For run
bot.polling()
