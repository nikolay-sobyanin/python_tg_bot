from loader import bot
from telebot.types import Message, InputMediaPhoto, ReplyKeyboardRemove
from utils.parsers import parser_hotels, parser_urls_photos
from utils import user_data
from keyboards import inline
from requests.exceptions import HTTPError, ConnectionError
from database import db_worker
from utils.logging.logger import my_logger
from geopy.distance import distance


def send_results(message: Message, sort_order) -> None:
    bot.send_message(message.from_user.id, 'Ищу отели...\nПодожди немного')
    user_data.set_data(message, 'sort_order', sort_order)
    data = user_data.get_all_value(message)

    try:
        hotels = parser_hotels.find_hotels(**data)
    except (HTTPError, ConnectionError, ValueError) as exc:
        msg_text = str(exc)
        bot.send_message(message.from_user.id, msg_text)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
        my_logger.error(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                        f'Ошибка соединения с сервером.')
    except KeyError:
        msg_text = 'Не могу обработать ответ от сервера...\nКоманда сброшена. Выполни запрос позже.'
        bot.send_message(message.from_user.id, msg_text)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
        my_logger.error(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                        f'Ошибка обработки информации на сервере.')
    else:
        for hotel in hotels:
            msg_text = f'Название отеля: {hotel["name"]}\n' \
                       f'Адрес: {hotel["address"]}\n' \
                       f'Стоимость одних суток: {hotel["rate"]}\n' \
                       f'Стоимость за весь период проживания: {hotel["rate_all"]}\n'
            markup = inline.url.get_markup(text=hotel['name'], url=hotel['url'])
            bot.send_message(message.from_user.id, msg_text, disable_web_page_preview=True, reply_markup=markup)

            if data['need_photos'].lower() == 'да':
                urls_photos = parser_urls_photos.find_urls_photos(hotel['id'], data['count_photos'])
                medias = [InputMediaPhoto(url_photo) for url_photo in urls_photos]
                bot.send_media_group(message.from_user.id, medias)

        db_worker.add_row(
            user_id=message.from_user.id,
            name_cmd=user_data.get_one_value(message, 'name_cmd'),
            hotels=';'.join([hotel['name'] for hotel in hotels])
        )
        bot.send_message(message.from_user.id, 'Поиск закончен!', reply_markup=ReplyKeyboardRemove())


def send_results_price_coordinate(message: Message, sort_order) -> None:
    bot.send_message(message.from_user.id, 'Ищу отели...\nПодожди немного')
    user_data.set_data(message, 'sort_order', sort_order)
    data = user_data.get_all_value(message)

    try:
        hotels = parser_hotels.find_hotels_price_coordinate(**data)
    except (HTTPError, ConnectionError, ValueError) as exc:
        msg_text = str(exc)
        bot.send_message(message.from_user.id, msg_text)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
        my_logger.error(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                        f'Ошибка соединения с сервером.')
    except KeyError:
        msg_text = 'Не могу обработать ответ от сервера...\nКоманда сброшена. Выполни запрос позже.'
        bot.send_message(message.from_user.id, msg_text)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
        my_logger.error(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                        f'Ошибка обработки информации на сервере.')
    else:
        city_coordinate = user_data.get_one_value(message, 'city_coordinate')
        min_dist, max_dist = user_data.get_one_value(message, 'distance_range')
        min_dist, max_dist = float(min_dist), float(max_dist)
        dist = distance(city_coordinate, hotel['hotel_coordinate']).km
        for hotel in hotels:
            msg_text = f'Название отеля: {hotel["name"]}\n' \
                       f'Адрес: {hotel["address"]}\n' \
                       f'Стоимость одних суток: {hotel["rate"]}\n' \
                       f'Стоимость за весь период проживания: {hotel["rate_all"]}\n'
            markup = inline.url.get_markup(text=hotel['name'], url=hotel['url'])
            bot.send_message(message.from_user.id, msg_text, disable_web_page_preview=True, reply_markup=markup)

            if data['need_photos'].lower() == 'да':
                urls_photos = parser_urls_photos.find_urls_photos(hotel['id'], data['count_photos'])
                medias = [InputMediaPhoto(url_photo) for url_photo in urls_photos]
                bot.send_media_group(message.from_user.id, medias)

        db_worker.add_row(
            user_id=message.from_user.id,
            name_cmd=user_data.get_one_value(message, 'name_cmd'),
            hotels=';'.join([hotel['name'] for hotel in hotels])
        )
        bot.send_message(message.from_user.id, 'Поиск закончен!', reply_markup=ReplyKeyboardRemove())
