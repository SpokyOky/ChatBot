import telebot
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')
bot = telebot.TeleBot(cfg['telegram']['token'])

business_list = ['delo1', 'delo2', 'delo3', 'delo4', 'delo5']
change_index = -12312


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Салам дядя')


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


@bot.message_handler(commands=['view'])
def view_message(message):
    biz_list = 'Список дел:\n'
    i = 1
    for biz in business_list:
        biz_list += str(i) + '. ' + biz + '\n'
        i += 1
    bot.send_message(message.chat.id, biz_list)


bot.polling()
