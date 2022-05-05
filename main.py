# -*- coding: utf-8 -*-

import telebot
from telebot import types
import settings

try:
    from local_config import TOKEN
except ImportError:
    exit('Do copy paste local_config.py.default (local_config.py) and set TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=list(settings.COMMAND))
def command_message(message):
    command = message.text[1:]
    bot.send_message(message.chat.id, settings.COMMAND[command]['answer'])


@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                               'text', 'location', 'contact', 'sticker'])
def error_message(message):
    bot.send_message(message.chat.id, settings.DEFAULT_MESSAGE)


bot.infinity_polling()
