from loader import bot
from states.lowprice import UserLowpriceState
from telebot.types import Message, InputMediaPhoto
from config_data.config import FORMAT_DATE
from utils.misc.parser_cities import find_cities
from keyboards.inline.cities import get_inline_cities_keyboard
from keyboards.inline.date import get_inline_date_keyboard
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from keyboards.reply.reply_answers import get_reply_answers_keyboard
from utils.misc.parser_hotels import find_hotels
from keyboards.inline.url import get_inline_url_keyboard
from utils.misc.parser_urls_photos import find_urls_photos


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserLowpriceState.city, message.chat.id)
    msg_text = 'Начнем поиск!\n' \
               'ВАЖНО! Временно поиск отелей в России недоступен.\n\n' \
               'В каком городе искать отели?\n' \
               'Чтобы мне было проще укажи страну, регион, город на английском языке.'
    bot.send_message(message.from_user.id, msg_text)


@bot.message_handler(state=UserLowpriceState.city)
def get_city(message: Message) -> None:
    cities = find_cities(message.text)
    markup = get_inline_cities_keyboard(cities)
    msg_text = 'Уточни, пожалуйста:'
    bot.send_message(message.from_user.id, msg_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'city')
def callback_city(call) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['city_name'] = call.data.split(':')[1]
        data['destination_id'] = call.data.split(':')[2]
        bot.edit_message_text(f'Ты выбрал город:{data["city_name"]}', call.message.chat.id, call.message.message_id)

    bot.set_state(call.from_user.id, UserLowpriceState.check_in, call.message.chat.id)
    get_check_in(call)


@bot.message_handler(state=UserLowpriceState.check_in)
def get_check_in(message: Message) -> None:
    msg_text = 'Выбери дату заезда?'
    bot.send_message(message.from_user.id, msg_text)
    calendar, step = get_inline_date_keyboard(calendar_id=1)
    bot.send_message(message.from_user.id, f'Выберите {step}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def callback_calendar_check_in(call):
    enter_date, key, step = DetailedTelegramCalendar(calendar_id=1).process(call.data)
    if not enter_date and key:
        bot.edit_message_text(f'Выбери {LSTEP[step]}', call.message.chat.id, call.message.message_id,
                              reply_markup=key)
    else:
        bot.edit_message_text(f'Ты выбрал дату: {enter_date.strftime("%d.%m.%Y")}',
                              call.message.chat.id,
                              call.message.message_id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_in'] = enter_date.strftime(FORMAT_DATE)

        bot.set_state(call.from_user.id, UserLowpriceState.check_out, call.message.chat.id)
        get_check_out(call)


@bot.message_handler(state=UserLowpriceState.check_out)
def get_check_out(message: Message) -> None:
    msg_text = 'Выбери дату отъезда?'
    bot.send_message(message.from_user.id, msg_text)
    calendar, step = get_inline_date_keyboard(calendar_id=2)
    bot.send_message(message.from_user.id, f'Выберите {step}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def callback_calendar_check_out(call):
    enter_date, key, step = DetailedTelegramCalendar(calendar_id=2).process(call.data)
    if not enter_date and key:
        bot.edit_message_text(f'Выбери {LSTEP[step]}', call.message.chat.id, call.message.message_id,
                              reply_markup=key)
    else:
        bot.edit_message_text(f'Ты выбрал дату: {enter_date.strftime("%d.%m.%Y")}',
                              call.message.chat.id,
                              call.message.message_id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_out'] = enter_date.strftime(FORMAT_DATE)

        bot.set_state(call.from_user.id, UserLowpriceState.count_hotels, call.message.chat.id)
        msg_text = 'Сколько найти отелей?'
        markup = get_reply_answers_keyboard([str(i) for i in range(2, 6)])
        bot.send_message(call.from_user.id, msg_text, reply_markup=markup)


@bot.message_handler(state=UserLowpriceState.count_hotels)
def get_count_hotels(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 5):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count_hotels'] = message.text

        bot.set_state(message.from_user.id, UserLowpriceState.need_photos, message.chat.id)
        msg_text = 'Фото отелей прикрепить?'
        markup = get_reply_answers_keyboard(['Да', 'Нет'])
        bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
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
        markup = get_reply_answers_keyboard([str(i) for i in range(4, 11, 2)])
        bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
    elif message.text.lower() == 'нет':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photos'] = message.text

        send_hotels(message)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


@bot.message_handler(state=UserLowpriceState.count_photos)
def get_count_photos(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 10):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count_photos'] = message.text

        send_hotels(message)
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)


def send_hotels(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Ищу отели...\nПодожди немного')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['sort_order'] = 'PRICE'
        hotels = find_hotels(**data)

        for hotel in hotels:
            msg_text = f'Название отеля: {hotel["name"]}\n' \
                       f'Адрес: {hotel["address"]}\n' \
                       f'Стоимость одних суток: {hotel["rate"]}\n' \
                       f'Стоимость за весь период проживания: {hotel["rate_all"]}\n'
            markup = get_inline_url_keyboard(text=hotel['name'], url=hotel['url'])
            bot.send_message(message.from_user.id, msg_text, disable_web_page_preview=True, reply_markup=markup)
            if data['need_photos'].lower() == 'да':
                urls_photos = find_urls_photos(hotel['id'], data['count_photos'])
                medias = [InputMediaPhoto(url_photo) for url_photo in urls_photos]
                bot.send_media_group(message.from_user.id, medias)

    bot.send_message(message.from_user.id, 'Поиск закончен!')
    bot.set_state(message.from_user.id, None, message.chat.id)
