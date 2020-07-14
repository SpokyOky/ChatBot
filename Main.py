import telebot
import configparser
import json

cfg = configparser.ConfigParser()
cfg.read('config.ini')
bot = telebot.TeleBot(cfg['telegram']['token'])

name = ''

business_list = []

change_index = -12312


def update_file():
    with open(name + '_business_list.json', 'w') as update_business:
        json.dump(business_list, update_business)


@bot.message_handler(commands=['start'])
def start_message(message):
    global name
    name = message.from_user.first_name
    output = 'Салам ' + name
    try:
        with open(name + '_business_list.json') as input_file:
            data = json.load(input_file)
            for biz in data:
                business_list.append(biz)
        output += '\n Список дел удочно загружен'
    except Exception:
        output += '\n Не удалось загрузить ваши дела, создание нового списка'
    bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '''
    /add - добавить дело
    /delete - удалить дело
    /change - изменить дело
    /view - посмотреть все дела
    ''')


@bot.message_handler(commands=['add'])
def add_message(message):
    bot.send_message(message.chat.id, 'Что тебе нужно сделать?')
    bot.register_next_step_handler(message, get_add_business)


def get_add_business(message):
    global business_list
    business_list.append(str(message.text))
    update_file()
    bot.send_message(message.chat.id, 'Дело записано')


@bot.message_handler(commands=['delete'])
def delete_message(message):
    bot.send_message(message.chat.id, 'Укажите номер дела для удаления')
    bot.register_next_step_handler(message, get_delete_index)


def get_delete_index(message):
    index = -12312
    while index == -12312:
        try:
            index = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, 'Только номер, пожалуйста')
            continue
    try:
        business_list.pop(index - 1)
        update_file()
        bot.send_message(message.chat.id, 'Удалено')
    except Exception:
        bot.send_message(message.chat.id, 'Дела по такому номеру не найдено')


@bot.message_handler(commands=['change'])
def change_message(message):
    bot.send_message(message.chat.id, 'Укажите номер дела для изменения')
    bot.register_next_step_handler(message, get_change_index)


def get_change_index(message):
    global change_index
    index = -12312
    while index == -12312:
        try:
            index = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, 'Только номер, пожалуйста')
            continue
    try:
        business_list[index - 1]
        change_index = index - 1
        bot.send_message(message.chat.id, '''
        Для изменения позиции дела введите позицию, на которую нужно его переместить
Для изменения названия дела введите его новое название
        ''')
        bot.register_next_step_handler(message, get_change_instructions)
    except Exception:
        bot.send_message(message.chat.id, 'Дела по такому номеру не найдено')


def get_change_instructions(message):
    try:
        res = int(message.text)
        temp = business_list[change_index]
        business_list.pop(change_index)
        business_list.insert(res - 1, temp)
        bot.send_message(message.chat.id, 'Дело перемещено')
    except Exception:
        business_list[change_index] = message.text
        bot.send_message(message.chat.id, 'Название изменено')
    update_file()


@bot.message_handler(commands=['view'])
def view_message(message):
    biz_list = 'Список дел:\n'
    i = 1
    for biz in business_list:
        biz_list += str(i) + '. ' + biz + '\n'
        i += 1
    bot.send_message(message.chat.id, biz_list)


bot.polling()
