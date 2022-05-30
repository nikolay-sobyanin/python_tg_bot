import telebot
from config import BOT_TOKEN
from botrequests.lowprice import CmdLowprice

bot = telebot.TeleBot(BOT_TOKEN)
list_commands = ['start', 'help', 'lowprice', 'highprice', 'bestdeal', 'history', 'reset']

states_users = {}  # user


def add_user(user_id: int, command: str, step: str):
    states_users[user_id] = {
        'command': command,
        'step': step,
        'data': {}
    }


@bot.message_handler(commands=['reset'])
def reset_state(message):
    bot.send_message(message.chat.id, 'Сброс состояния')


@bot.message_handler(commands=list_commands, func=lambda x: False)
def block_enter_commands(message):
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
def lowprice_start(message):
    pass


if __name__ == '__main__':
    bot.infinity_polling()
