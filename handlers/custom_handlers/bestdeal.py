from loader import bot
from states.bestdeal import UserBestdealState
from telebot.types import Message, CallbackQuery
from utils import find_hotels, find_cities, user_data, date_worker
from keyboards import inline, reply
import re
from utils.logging.logger import my_logger

cities = list()  # Переменная модуля для записи найденных городов, далее её удаляю


@bot.message_handler(commands=['bestdeal'])
def bot_highprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserBestdealState.city, message.chat.id)
    user_data.set_data(message, 'name_cmd', message.text)
    msg_text = 'Начнем поиск!\n' \
               'ВАЖНО! Временно поиск отелей в России недоступен.\n\n' \
               'В каком городе искать отели?\n' \
               'Чтобы мне было проще укажи страну, регион, город на английском языке.'
    bot.send_message(message.from_user.id, msg_text)
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Запустил команду бота /bestdeal.')


@bot.message_handler(state=UserBestdealState.city)
def city(message: Message) -> None:
    global cities
    cities = find_cities.get_send_results(message)


@bot.callback_query_handler(state=UserBestdealState.city, func=None)
def callback_city(call: CallbackQuery) -> None:
    global cities
    destination_id = call.data
    city_name = None
    city_coordinate = None
    for _city in cities:
        if _city['destination_id'] == destination_id:
            city_name = _city['city_name']
            city_coordinate = _city['city_coordinate']
            break
    del cities

    user_data.set_data(call, 'destination_id', destination_id)
    user_data.set_data(call, 'city_name', city_name)
    user_data.set_data(call, 'city_coordinate', city_coordinate)

    bot.edit_message_text(f'Ты выбрал город: {city_name}', call.message.chat.id, call.message.message_id)
    my_logger.info(f'user id: {call.from_user.id}, user name: {call.from_user.full_name}. '
                   f'Выбрал город: {city_name}.')

    bot.set_state(call.from_user.id, UserBestdealState.check_in, call.message.chat.id)
    check_in(call)


@bot.message_handler(state=UserBestdealState.check_in)
def check_in(message: Message or CallbackQuery) -> None:
    msg_text = 'Выбери дату заезда?'
    bot.send_message(message.from_user.id, msg_text)
    inline.date.send_calendar(message)


@bot.callback_query_handler(state=UserBestdealState.check_in, func=inline.date.callback_calendar())
def callback_calendar_check_in(call) -> None:
    enter_date = inline.date.next_step_calendar(call)

    if enter_date:
        user_data.set_data(call, 'check_in', enter_date)
        bot.set_state(call.from_user.id, UserBestdealState.check_out, call.message.chat.id)
        my_logger.info(f'user id: {call.from_user.id}, user name: {call.from_user.full_name}. '
                       f'Выбрал дату заезда: {enter_date}')
        check_out(call)


@bot.message_handler(state=UserBestdealState.check_out)
def check_out(message: Message or CallbackQuery) -> None:
    msg_text = 'Выбери дату отъезда?'
    bot.send_message(message.from_user.id, msg_text)

    min_date = date_worker.get_date_obj(user_data.get_one_value(message, 'check_in'))
    min_date = date_worker.get_delta_date(days=1, start_date=min_date)
    inline.date.send_calendar(message, min_date=min_date)


@bot.callback_query_handler(state=UserBestdealState.check_out, func=inline.date.callback_calendar())
def callback_calendar_check_out(call: CallbackQuery) -> None:
    min_date = date_worker.get_date_obj(user_data.get_one_value(call, 'check_in'))
    min_date = date_worker.get_delta_date(days=1, start_date=min_date)
    enter_date = inline.date.next_step_calendar(call, min_date=min_date)

    if enter_date:
        user_data.set_data(call, 'check_out', enter_date)
        my_logger.info(f'user id: {call.from_user.id}, user name: {call.from_user.full_name}. '
                       f'Выбрал дату отъезда: {enter_date}')

        bot.set_state(call.from_user.id, UserBestdealState.price_range, call.message.chat.id)
        msg_text = 'Введи диапазон цен в $ за одну ночь в формате min - max\nНапример, 250 - 500'
        bot.send_message(call.from_user.id, msg_text)


@bot.message_handler(state=UserBestdealState.price_range)
def price_range(message: Message) -> None:
    text = message.text.replace(' ', '')
    pattern = r'^\d{1,5}-\d{1,5}$'
    if re.match(pattern, text):
        min_price, max_price = text.split('-')
        if int(min_price) < int(max_price):
            bot.set_state(message.from_user.id, UserBestdealState.distance_range, message.chat.id)
            user_data.set_data(message, 'price_range', (min_price, max_price))
            msg_text = 'Введи диапазон расстояний в км в формате min - max\nНапример, 0.2 - 1.5'
            bot.send_message(message.from_user.id, msg_text)
            my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                           f'Ввел диапазон цен: {min_price} - {max_price}')
            return

    error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
    bot.send_message(message.from_user.id, error_text)
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Неверный ввод диапазона цен.')


@bot.message_handler(state=UserBestdealState.distance_range)
def distance_range(message: Message) -> None:
    text = message.text.replace(' ', '')
    text = text.replace(',', '.')
    pattern = r'^(\d{1,2}[.])?\d{1,2}-(\d{1,2}[.])?\d{1,2}$'
    if re.match(pattern, text):
        min_dist, max_dist = text.split('-')
        if float(min_dist) < float(max_dist):
            bot.set_state(message.from_user.id, UserBestdealState.count_hotels, message.chat.id)
            user_data.set_data(message, 'distance_range', (min_dist, max_dist))
            msg_text = 'Сколько найти отелей?'
            markup = reply.reply_answers.get_markup([str(i) for i in range(2, 6)])
            bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
            my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                           f'Ввел диапазон расстояний: {min_dist} - {max_dist}')
            return

    error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
    bot.send_message(message.from_user.id, error_text)
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Неверный ввод диапазона расстояний.')


@bot.message_handler(state=UserBestdealState.count_hotels)
def count_hotels(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 5):
        user_data.set_data(message, 'count_hotels', message.text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Выбрал количество отелей: {message.text}')

        bot.set_state(message.from_user.id, UserBestdealState.need_photos, message.chat.id)
        msg_text = 'Фото отелей прикрепить?'
        markup = reply.reply_answers.get_markup(['Да', 'Нет'])
        bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Неверный ввод количества отелей.')


@bot.message_handler(state=UserBestdealState.need_photos)
def need_photos(message: Message) -> None:
    if message.text.lower() == 'да':
        user_data.set_data(message, 'need_photos', message.text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Выбрал необходимость фото: {message.text}')

        bot.set_state(message.from_user.id, UserBestdealState.count_photos, message.chat.id)
        msg_text = 'Сколько фото прикрепить?'
        markup = reply.reply_answers.get_markup([str(i) for i in range(4, 11, 2)])
        bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
    elif message.text.lower() == 'нет':
        user_data.set_data(message, 'need_photos', message.text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Выбрал необходимость фото: {message.text}')
        find_hotels.send_results_price_coordinate(message, sort_order='PRICE')
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Закончил выполнение команды /bestdeal')
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Неверный ввод необходимости фото.')


@bot.message_handler(state=UserBestdealState.count_photos)
def count_photos(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 10):
        user_data.set_data(message, 'count_photos', message.text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Выбрал количество фото отелей: {message.text}')
        find_hotels.send_results_price_coordinate(message, sort_order='PRICE')
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Закончил выполнение команды /bestdeal')
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Неверный ввод количества фото.')
