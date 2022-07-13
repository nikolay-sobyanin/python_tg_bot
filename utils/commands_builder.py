import re
import json
from loader import bot
from telebot.types import Message, CallbackQuery
from .misc.api_hotels import APIHotels
from config_data.config import START_URL, HEADERS, LOCALE, CURRENCY
from requests.exceptions import HTTPError, ConnectionError
from .logging.logger import my_logger


class FindCity:

    @staticmethod
    def start(message: Message) -> None:
        msg_text = 'В каком городе искать отели?\n' \
                   'Чтобы мне было проще укажи страну, регион, город на английском языке.\n\n' \
                   'ВАЖНО! Временно поиск отелей в России недоступен.'
        bot.send_message(message.from_user.id, msg_text)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): начал поиск городов.')

    @staticmethod
    def _parser_cities(city: str) -> list:
        url = START_URL + '/locations/v2/search'
        querystring = {'query': city, 'locale': LOCALE, 'currency': CURRENCY}
        data_text = APIHotels.request_api(url=url, headers=HEADERS, querystring=querystring)

        pattern = r'(?<="CITY_GROUP",).+?[\]]'
        find = re.search(pattern, data_text)
        if find:
            data_json = json.loads(f"{{{find[0]}}}")

            cities = list()
            for city in data_json['entities']:
                city_name = re.sub(r'</?span.*?>', '', city['caption'])
                cities.append({
                    'city_name': city_name,
                    'destination_id': city['destinationId'],
                    'city_coordinate': (city['latitude'], city['longitude'])
                })

            if not cities:
                raise ValueError('Я не нашел города.\nУточни запрос.')

            return cities
        else:
            raise HTTPError('Не могу обработать ответ от сервера...\nКоманда сброшена. Выполни запрос позже..')

    @staticmethod
    def find_cities(message: Message) -> None:
        msg_text = 'Подожди, ищу города...'
        bot.send_message(message.from_user.id, msg_text)

        try:
            cities = FindCity._parser_cities(message.text)
        except (HTTPError, ConnectionError) as exc:
            bot.send_message(message.from_user.id, str(exc))
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.reset_data(message.from_user.id, message.chat.id)
            my_logger.error(f'{message.from_user.full_name} (id: {message.from_user.id}): '
                            f'ошибка соединения с сервером.')
        except ValueError as exc:
            bot.send_message(message.from_user.id, str(exc))
            my_logger.error(f'{message.from_user.full_name} (id: {message.from_user.id}): '
                            f'Города по запросу не найдены. Требуется повтор ввода.')
        else:
            markup = inline.cities.get_markup(cities)
            msg_text = 'Уточни, пожалуйста:'
            bot.send_message(message.from_user.id, msg_text, reply_markup=markup)

