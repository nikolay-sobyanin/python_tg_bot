import os
import telebot

BOT_NAME = os.getenv('BOT_USERNAME')
TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Привет! Вы запустили бота, который производит поиск отлей.\n'
                                      'Ознакомься с инструкция по работе с ним - /help.')


@bot.message_handler(commands=['help'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Инструкция по работе бота.\n'
                                      '/lowprice - узнать топ самых дешёвых отелей в городе\n'
                                      '/highprice - узнать топ самых дорогих отелей в городе\n'
                                      '/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра\n'
                                      '/history - вывод истории поиска отелей')


if __name__ == '__main__':
    bot.infinity_polling()
