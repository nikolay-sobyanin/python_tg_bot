import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, datetime, timedelta

from config import BOT_TOKEN, FORMAT_DATE
from botrequests.lowprice import CmdLowprice

bot = telebot.TeleBot(BOT_TOKEN)
BLOCK_COMMANDS = ['start', 'lowprice', 'highprice', 'bestdeal', 'history']

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
    bot.send_message(message.chat.id, f'Прости, я не такой умный :(\n'
                                      f'Я понимаю только текс, но я буду учиться :)')


@bot.message_handler(commands=BLOCK_COMMANDS, func=lambda message: message.chat.id in users)
def block_commands(message):
    """
    Болокируем ввод команд находясь в сценарии какой-либо команды
    :param message:
    """
    user_id = message.chat.id
    command_name = users[user_id].COMMAND_NAME
    bot.send_message(message.chat.id, f'Ты выполняешь команду - {command_name}.\n'
                                      f'Если хочешь закончить, выполни /reset')


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Я помогаю находить отели!\n'
                                      'Ознакомься с моими командами - /help.')


@bot.message_handler(commands=['help'])
def cmd_help(message):
    user_id = message.chat.id
    if user_id in users:
        command_name = users[user_id].COMMAND_NAME
        bot.send_message(message.chat.id, f'Ты ты выполняешь команду /{command_name}\n'
                                          f'Если хочешь прервать её, используй /reset')
    else:
        bot.send_message(message.chat.id, 'Посмотри что я умею:\n'
                                          '/lowprice - найду самые дешёвые отели в городе\n'
                                          '/highprice - найду самые дорогие отели в городе\n'
                                          '/bestdeal - найду отели лучшие по цене и расположению от центра\n'
                                          '/history - покажу тебе истории поиска отелей\n'
                                          '/reset - сброшу текущий команду')


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
        bot.send_message(message.chat.id, f'Ты досрочно завершил поиск /{command_name}!\n'
                                          f'Ты можешь начать новый, /help тебе поможет')
    else:
        bot.send_message(message.chat.id, f'Упс... Ты не выполняешь поиск...')


@bot.message_handler(commands=['lowprice'])
def cmd_lowprice_start(message):
    """
    Запуск сценария команды lowprice
    :param message:
    """
    user_id = message.chat.id
    users[user_id] = CmdLowprice()
    result = users[user_id].start()
    reply_user(user_id, result)


@bot.message_handler(func=lambda message: check_user(message.chat.id, CmdLowprice))
def cmd_lowprice_run(message):
    """
    Движение по сценарию команды lowprice
    :param message:
    """
    user_id = message.chat.id
    try:
        result = users[user_id].run(message.text)
    except:
        raise
    reply_user(user_id, result)


def reply_user(user_id: int, result: dict):
    """
    Ответ пользователю
    :param user_id: id пользователя
    :param result: словарь с ответом от обработчика {'step': <name_step>, 'message_text': <text>, 'keyboard': <type>},
    но если step = 'finish' {'step': 'finish', 'hotels': []}
    """
    if result['step'] == 'finish':
        data_hotels = result['data_hotels']

        if not data_hotels['hotels_found']:
            bot.send_message(user_id, data_hotels['text_error'])
            cmd_reset()
        markup = create_inline_keyboard()
        bot.send_message(user_id, 'Закончил поиск!', disable_web_page_preview=True, reply_markup=markup)

        medias = [types.InputMediaPhoto(data_hotels['hotels'][0]['url_photos'][0])]
        bot.send_media_group(user_id, medias)
        users.pop(user_id)
        return

    if result['keyboard']['type'] is None:
        bot.send_message(user_id, result['message_text'])
    elif result['keyboard']['type'] == 'date':
        bot.send_message(user_id, result['message_text'])
        create_calendar_keyboard(user_id)
    elif result['keyboard']['type'] == 'reply':
        markup = create_reply_keyboard(result['answers'])
        bot.send_message(user_id, result['message_text'], reply_markup=markup)


def send_result():
    pass


def create_inline_keyboard(text, url):
    markup = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text=text, url=url)
    markup.add(url_button)
    return markup


def create_reply_keyboard(answers: list):
    """
    Генератор клавиатуры с определенными ответами
    :param answers: список ответов
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for answer in answers:
        markup.add(answer)
    return markup


#  Создание клавиатуры ввода даты
def get_min_max_date(user_id: int):
    data = users[user_id].data
    if 'enter_date_from' in data:
        min_date = datetime.strptime(data['enter_date_from'], FORMAT_DATE).date()
    else:
        min_date = date.today()
    max_date = date.today() + timedelta(days=180)
    return min_date, max_date


def create_calendar_keyboard(user_id: int):
    """
    Генератор инлайн клавиатуры для введения даты
    :param user_id: id пользователя
    :return:
    """
    min_date, max_date = get_min_max_date(user_id)
    calendar, step = DetailedTelegramCalendar(min_date=min_date, max_date=max_date).build()
    bot.send_message(user_id, f'Выбери {LSTEP[step]}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def callback_calendar_keyboard(call):
    """
    Обработка даты от инлайн клавиатуры и дальнейшее движение по сценарию
    :param call:
    """
    user_id = call.message.chat.id
    min_date, max_date = get_min_max_date(user_id)
    enter_date, key, step = DetailedTelegramCalendar(min_date=min_date, max_date=max_date).process(call.data)
    if not enter_date and key:
        bot.edit_message_text(f'Выбери {LSTEP[step]}', call.message.chat.id, call.message.message_id, reply_markup=key)
    else:
        bot.edit_message_text(f'Ты выбрал дату: {enter_date.strftime("%d.%m.%Y")}',
                              call.message.chat.id,
                              call.message.message_id)
        date_str = enter_date.strftime(FORMAT_DATE)
        result = users[user_id].run(date_str)
        reply_user(user_id, result)


if __name__ == '__main__':
    bot.infinity_polling()
