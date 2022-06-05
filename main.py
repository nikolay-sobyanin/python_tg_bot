import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from config import BOT_TOKEN
from botrequests.lowprice import CmdLowprice

bot = telebot.TeleBot(BOT_TOKEN)
BLOCK_COMMANDS = ['lowprice', 'highprice', 'bestdeal', 'start']

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


# Не работает! Почему?
# func= lambda message: message.content_type != 'text'
@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice',
                                    'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title',
                                    'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
                                    'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                                    'migrate_from_chat_id', 'pinned_message'])
def block_message(message):
    bot.send_message(message.chat.id, f'Упс... Ошибка!\nБот понимает только текстовые сообщения!')


@bot.message_handler(commands=BLOCK_COMMANDS, func=lambda message: message.chat.id in users)
def block_commands(message):
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
    user_id = message.chat.id
    if user_id in users:
        command_name = users[user_id].COMMAND_NAME
        users.pop(user_id)
        bot.send_message(message.chat.id, f'Вы покинули сценарий команды /{command_name}')
    else:
        bot.send_message(message.chat.id, f'Вы не находитесь в сценарии команды...')


@bot.message_handler(commands=['lowprice'])
def cmd_lowprice_start(message):
    user_id = message.chat.id
    users[user_id] = CmdLowprice()
    result = users[user_id].start()
    bot.send_message(user_id, result['message_text'])


@bot.message_handler(func=lambda message: check_user(message.chat.id, CmdLowprice))
def cmd_lowprice_run(message):
    user_id = message.chat.id
    result = users[user_id].run(message.text)
    result_handler(user_id, result)


def result_handler(user_id, result):
    if result['step'] == 'finish':
        for i in range(1, 6):
            bot.send_message(user_id, f'Результат № {i}!')
        users.pop(user_id)
        return

    if result['keyboard']['type'] is None:
        bot.send_message(user_id, result['message_text'])

    if result['keyboard']['type'] == 'date':
        bot.send_message(user_id, result['message_text'])
        create_calendar(user_id)

    if result['keyboard']['type'] == 'reply':
        markup = generate_markup(result['keyboard']['answers'])
        bot.send_message(user_id, result['message_text'], reply_markup=markup)


def generate_markup(answers):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    for answer in answers:
        markup.add(answer)
    return markup


def create_calendar(user_id):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(user_id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)
        user_id = c.message.chat.id
        result_1 = users[user_id].run(str(result))
        result_handler(user_id, result_1)


if __name__ == '__main__':
    bot.infinity_polling()
