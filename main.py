import telebot
import config
from data_base.db_worker import ControlState

bot = telebot.TeleBot(config.BOT_TOKEN)
state = ControlState(config.PATH_DB)

list_commands = ['start', 'help', 'lowprice', 'highprice', 'bestdeal', 'history', 'reset']


@bot.message_handler(commands=['reset'])
def reset_state(message):
    bot.send_message(message.chat.id, 'Сброс состояния')


@bot.message_handler(commands=list_commands, func=lambda x: True)
def check_state(message):
    bot.send_message(message.chat.id, 'Проверка состояния')


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Привет! Ты запустили бота, который производит поиск отлей.\n'
                                      'Ознакомься с его командами - /help.')


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, 'Инструкция по работе бота.\n'
                                      '/lowprice - поиск топ самых дешёвых отелей в городе\n'
                                      '/highprice - поиск топ самых дорогих отелей в городе\n'
                                      '/bestdeal - поиск отелей наиболее подходящих по цене и расположению от центра\n'
                                      '/history - вывод истории поиска отелей\n'
                                      '/reset - сброс текущего поиска')


@bot.message_handler(commands=['lowprice'])
def cmd_lowprice(message):
    state.set_state(message.chat.id, 'lowprice', 'step_1')
    bot.send_message(message.chat.id, 'Ты выбрал команду lowprice')


@bot.message_handler(commands=['highprice'])
def cmd_highprice(message):
    bot.send_message(message.chat.id, 'Ты выбрал команду highprice')


@bot.message_handler(commands=['bestdeal'])
def cmd_bestdeal(message):
    bot.send_message(message.chat.id, 'Ты выбрал команду bestdeal')


@bot.message_handler(commands=['history'])
def cmd_history(message):
    bot.send_message(message.chat.id, 'Ты выбрал команду bestdeal')


if __name__ == '__main__':
    bot.infinity_polling()
