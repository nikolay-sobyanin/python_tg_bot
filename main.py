from pprint import pprint

import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, datetime, timedelta

from config import BOT_TOKEN, FORMAT_DATE
from botrequests.lowprice import CmdLowprice

bot = telebot.TeleBot(BOT_TOKEN)
BLOCK_COMMANDS = ['lowprice', 'highprice', 'bestdeal', 'start']

"""
Словарь пользователей, которые находятся в сценарии команды
key: id пользователя
value: объект обработчик сообщений от пользователя
"""
users = {}


def check_user(user_id: int, cls):
    if user_id in users:
        return isinstance(users[user_id], cls)
    else:
        return False


# Не работает! Почему?
# func= lambda message: message.content_type != 'text'
@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice',
                                    'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title',
                                    'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
                                    'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                                    'migrate_from_chat_id', 'pinned_message'])
def block_message(message):
    """
    Блокируем все сообщения кроме content_types='text'
    :param message:
    """
    bot.send_message(message.chat.id, f'Упс... Ошибка!\nБот понимает только текстовые сообщения!')


@bot.message_handler(commands=BLOCK_COMMANDS, func=lambda message: message.chat.id in users)
def block_commands(message):
    """
    Болокируем ввод команд находясь в сценарии какой-либо команды
    :param message:
    """
    user_id = message.chat.id
    command_name = users[user_id].COMMAND_NAME
    bot.send_message(message.chat.id, f'Вы находитесь в сценарии команды - {command_name}.\n'
                                      f'Введи команду /reset, чтобы выйти из сценария.')


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Я помогу тебе найти отели!\n'
                                      'Ознакомься с моими командами - /help.')


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
    """
    Сброс команды со сценарием
    :param message:
    """
    user_id = message.chat.id
    if user_id in users:
        command_name = users[user_id].COMMAND_NAME
        users.pop(user_id)
        bot.send_message(message.chat.id, f'Вы покинули сценарий команды /{command_name}')
    else:
        bot.send_message(message.chat.id, f'Вы не находитесь в сценарии команды...')


@bot.message_handler(commands=['lowprice'])
def cmd_lowprice_start(message):
    """
    Запуск сценария команды lowprice
    :param message:
    """
    user_id = message.chat.id
    users[user_id] = CmdLowprice()
    result = users[user_id].start()
    bot.send_message(user_id, result['message_text'])


@bot.message_handler(func=lambda message: check_user(message.chat.id, CmdLowprice))
def cmd_lowprice_run(message):
    """
    Движение по сценарию команды lowprice
    :param message:
    """
    user_id = message.chat.id
    result = users[user_id].run(message.text)
    reply_user(user_id, result)


def reply_user(user_id: int, result: dict):
    """
    Ответ пользователю
    :param user_id: id пользователя
    :param result: словарь с ответом от обработчика {}
    """
    if result['step'] == 'finish':
        data_hotels = result['data_hotels']

        if not data_hotels['hotels_found']:
            bot.send_message(user_id, data_hotels['text_error'])
            cmd_reset()
        pprint(data_hotels)
        markup = generate_inline_keyboard()
        bot.send_message(user_id, 'Закончил поиск!', disable_web_page_preview=True, reply_markup=markup)
        users.pop(user_id)
        return

    if result['keyboard']['type'] is None:
        bot.send_message(user_id, result['message_text'])
    elif result['keyboard']['type'] == 'date':
        bot.send_message(user_id, result['message_text'])
        generate_calendar_keyboard(user_id)
    elif result['keyboard']['type'] == 'reply':
        markup = generate_reply_keyboard(result['keyboard']['answers'])
        bot.send_message(user_id, result['message_text'], reply_markup=markup)
    else:
        raise TypeError


def generate_inline_keyboard():
    markup = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на hotels.ru", url="https://www.hotels.ru/")
    markup.add(url_button)
    return markup


def generate_reply_keyboard(answers: list):
    """
    Генератор клавиатуры с определенными ответами
    :param answers: список ответов
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for answer in answers:
        markup.add(answer)
    return markup


def get_min_max_date(user_id: int):
    if 'enter_date_from' in users[user_id].data:
        min_date = datetime.strptime(users[user_id].data['enter_date_from'], FORMAT_DATE).date()
    else:
        min_date = date.today()
    max_date = date.today() + timedelta(days=365)
    return min_date, max_date


def generate_calendar_keyboard(user_id: int):
    """
    Генератор инлайн клавиатуры для введения даты
    :param user_id: id пользователя
    :return:
    """
    min_date, max_date = get_min_max_date(user_id)
    calendar, step = DetailedTelegramCalendar(min_date=min_date, max_date=max_date).build()
    bot.send_message(user_id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def callback__calendar_keyboard(call):
    """
    Обработка даты от инлайн клавиатуры и дальнейшее движение по сценарию
    :param call:
    """
    user_id = call.message.chat.id
    min_date, max_date = get_min_max_date(user_id)
    enter_date, key, step = DetailedTelegramCalendar(min_date=min_date, max_date=max_date).process(call.data)
    if not enter_date and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif enter_date:
        bot.edit_message_text(f"Ты выбрал дату {enter_date.strftime(FORMAT_DATE)}",
                              call.message.chat.id,
                              call.message.message_id)
        result = users[user_id].run(enter_date.strftime(FORMAT_DATE))
        reply_user(user_id, result)


if __name__ == '__main__':
    bot.infinity_polling()
