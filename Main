import telebot
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')
bot = telebot.TeleBot(cfg['telegram']['token'])

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Салам дядя')

bot.polling()
