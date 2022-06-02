import telebot
from config import BOT_TOKEN
from botrequests.lowprice import CmdLowprice

bot = telebot.TeleBot(BOT_TOKEN)
list_commands = ['start', 'help', 'lowprice', 'highprice', 'bestdeal', 'history', 'reset']

"""
dict of users
key: user_id
value: cmd_object
"""
users = {}


def check_user(user_id: int, cls):
    if user_id in users:
        return isinstance(users[user_id], cls)
    else:
        return False


@bot.message_handler(commands=list_commands, func=lambda x: False)
def block_msg_types(message):
    bot.send_message(message.chat.id, 'Проверка состояния')


@bot.message_handler(commands=list_commands, func=lambda x: False)
def block_command(message):
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


@bot.message_handler(commands=['reset'])
def cmd_reset(message):
    bot.send_message(message.chat.id, 'Сброс состояния')


@bot.message_handler(commands=['lowprice'])
def cmd_lowprice_start(message):
    user_id = message.chat.id
    users[user_id] = CmdLowprice()
    msg = users[user_id].start()
    bot.send_message(user_id, msg)


@bot.message_handler(func=lambda message: check_user(message.chat.id, CmdLowprice))
def cmd_lowprice_run(message):
    user_id = message.chat.id
    msg = users[user_id].run(message)
    if msg == 'Мы закончили':
        users.pop(user_id)
        bot.send_message(user_id, 'Команда окончена')
    else:
        bot.send_message(user_id, msg)


if __name__ == '__main__':
    bot.infinity_polling()
