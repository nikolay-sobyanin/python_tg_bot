from loader import bot
from states.lowprice import UserLowpriceState
from telebot.types import Message, CallbackQuery
from utils import find_hotels, find_cities, user_data, date_worker
from keyboards import inline, reply


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserLowpriceState.city, message.chat.id)
    user_data.set_data(message, 'name_cmd', message.text)
    msg_text = 'Начнем поиск!\n' \
               'ВАЖНО! Временно поиск отелей в России недоступен.\n\n' \
               'В каком городе искать отели?\n' \
               'Чтобы мне было проще укажи страну, регион, город на английском языке.'
    bot.send_message(message.from_user.id, msg_text)


@bot.message_handler(state=UserLowpriceState.city)
def city(message: Message) -> None:
    find_cities.send_results(message)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'city')
def callback_city(call: CallbackQuery) -> None:
    user_data.set_data(call, 'city_name', call.data.split(':')[1])
    user_data.set_data(call, 'destination_id', call.data.split(':')[2])
    city_name = user_data.get_one_value(call, 'city_name')
    bot.edit_message_text(f'Ты выбрал город: {city_name}', call.message.chat.id, call.message.message_id)

    bot.set_state(call.from_user.id, UserLowpriceState.check_in, call.message.chat.id)
    check_in(call)


@bot.message_handler(state=UserLowpriceState.check_in)
def check_in(message: Message or CallbackQuery) -> None:
    msg_text = 'Выбери дату заезда?'
    bot.send_message(message.from_user.id, msg_text)
    inline.date.send_calendar(message, calendar_id=1)


@bot.callback_query_handler(func=inline.date.callback_calendar(calendar_id=1))
def callback_calendar_check_in(call) -> None:
    enter_date = inline.date.next_step_calendar(call, calendar_id=1)

    if enter_date:
        user_data.set_data(call, 'check_in', enter_date)
        bot.set_state(call.from_user.id, UserLowpriceState.check_out, call.message.chat.id)
        check_out(call)


@bot.message_handler(state=UserLowpriceState.check_out)
def check_out(message: Message or CallbackQuery) -> None:
    msg_text = 'Выбери дату отъезда?'
    bot.send_message(message.from_user.id, msg_text)

    min_date = date_worker.get_date_obj(user_data.get_one_value(message, 'check_in'))
    min_date = date_worker.get_delta_date(days=1, start_date=min_date)
    inline.date.send_calendar(message, calendar_id=2, min_date=min_date)


@bot.callback_query_handler(func=inline.date.callback_calendar(calendar_id=2))
def callback_calendar_check_out(call: CallbackQuery) -> None:
    min_date = date_worker.get_date_obj(user_data.get_one_value(call, 'check_in'))
    min_date = date_worker.get_delta_date(days=1, start_date=min_date)
    enter_date = inline.date.next_step_calendar(call, calendar_id=2, min_date=min_date)

    if enter_date:
        user_data.set_data(call, 'check_out', enter_date)

        bot.set_state(call.from_user.id, UserLowpriceState.count_hotels, call.message.chat.id)
        msg_text = 'Сколько найти отелей?'
        markup = reply.reply_answers.get_markup([str(i) for i in range(2, 6)])
        bot.send_message(call.from_user.id, msg_text, reply_markup=markup)


@bot.message_handler(state=UserLowpriceState.count_hotels)
def count_hotels(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 5):
        user_data.set_data(message, 'count_hotels', message.text)

        bot.set_state(message.from_user.id, UserLowpriceState.need_photos, message.chat.id)
        msg_text = 'Фото отелей прикрепить?'
        markup = reply.reply_answers.get_markup(['Да', 'Нет'])
        bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


@bot.message_handler(state=UserLowpriceState.need_photos)
def need_photos(message: Message) -> None:
    if message.text.lower() == 'да':
        user_data.set_data(message, 'need_photos', message.text)

        bot.set_state(message.from_user.id, UserLowpriceState.count_photos, message.chat.id)
        msg_text = 'Сколько фото прикрепить?'
        markup = reply.reply_answers.get_markup([str(i) for i in range(4, 11, 2)])
        bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
    elif message.text.lower() == 'нет':
        user_data.set_data(message, 'need_photos', message.text)
        find_hotels.send_results(message, sort_order='PRICE')
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


@bot.message_handler(state=UserLowpriceState.count_photos)
def count_photos(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 10):
        user_data.set_data(message, 'count_photos', message.text)
        find_hotels.send_results(message, sort_order='PRICE')
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)
