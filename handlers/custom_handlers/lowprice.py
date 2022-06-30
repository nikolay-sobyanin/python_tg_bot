from loader import bot
from states.lowprice import UserLowpriceState
from telebot.types import Message
import re
from config_data.config import PATTERN_DATE


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserLowpriceState.city, message.chat.id)
    msg_text = 'Начнем поиск!\n\n' \
               'В каком городе мне искать отели?\n' \
               'Чтобы я точно нашел укажи страну, регион, город.'
    bot.send_message(message.from_user.id, msg_text)


@bot.message_handler(state=UserLowpriceState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text

        bot.set_state(message.from_user.id, UserLowpriceState.check_in, message.chat.id)
        msg_text = 'Выбери дату заезда?'
        bot.send_message(message.from_user.id, msg_text)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


@bot.message_handler(state=UserLowpriceState.check_in)
def get_check_in(message: Message) -> None:
    if re.search(PATTERN_DATE, message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['check_in'] = message.text

        bot.set_state(message.from_user.id, UserLowpriceState.check_out, message.chat.id)
        msg_text = 'Выбери дату отъезда?'
        bot.send_message(message.from_user.id, msg_text)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


@bot.message_handler(state=UserLowpriceState.check_out)
def get_check_out(message: Message) -> None:
    if re.search(PATTERN_DATE, message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['check_out'] = message.text

        bot.set_state(message.from_user.id, UserLowpriceState.count_hotels, message.chat.id)
        msg_text = 'Сколько найти отелей?'
        bot.send_message(message.from_user.id, msg_text)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


@bot.message_handler(state=UserLowpriceState.count_hotels)
def get_count_hotels(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 5):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count_hotels'] = message.text

        bot.set_state(message.from_user.id, UserLowpriceState.need_photos, message.chat.id)
        msg_text = 'Фото отелей прикрепить?'
        bot.send_message(message.from_user.id, msg_text)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


@bot.message_handler(state=UserLowpriceState.need_photos)
def get_need_photos(message: Message) -> None:
    if message.text.lower() == 'да':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photos'] = message.text

        bot.set_state(message.from_user.id, UserLowpriceState.count_photos, message.chat.id)
        msg_text = 'Сколько фото прикрепить?'
        bot.send_message(message.from_user.id, msg_text)
    elif message.text.lower() == 'нет':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photos'] = message.text
            msg_text = f'Город - {data["city"]}\n' \
                       f'Дата заезда - {data["check_in"]}\n' \
                       f'Дата отъезда - {data["check_out"]}\n' \
                       f'Количество отелей - {data["count_hotels"]}\n'
            bot.send_message(message.from_user.id, msg_text)

        bot.set_state(message.from_user.id, None, message.chat.id)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


@bot.message_handler(state=UserLowpriceState.count_photos)
def get_count_photos(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 10):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count_photos'] = message.text
            msg_text = f'Город - {data["city"]}\n' \
                       f'Дата заезда - {data["check_in"]}\n' \
                       f'Дата отъезда - {data["check_out"]}\n' \
                       f'Количество отелей - {data["count_hotels"]}\n' \
                       f'Количество отелей - {data["count_photos"]}'
            bot.send_message(message.from_user.id, msg_text)

        bot.set_state(message.from_user.id, None, message.chat.id)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)
