import re
from requests.exceptions import ConnectionError, HTTPError
from botrequests.search_hotels import SearchHotels
from config import PATTERN_DATE


class CmdLowprice:
    COMMAND_NAME = 'lowprice'
    SCENARIO = {
        'start_step': 'enter_city',
        'enter_city': {
            'message': 'Начнем поиск!\n\n'
                       'В каком городе мне искать отели?\n'
                       'Чтобы я точно нашел его укажи страну, регион, город.',
            'keyboard': {'type': None},
            'next_step': 'enter_date_from'
        },
        'enter_date_from': {
            'message': 'Выбери дату заезда?',
            'keyboard': {'type': 'date'},
            'next_step': 'enter_date_to'
        },
        'enter_date_to': {
            'message': 'Выбери дату отъезда?',
            'keyboard': {'type': 'date'},
            'next_step': 'enter_count_hotels'
        },
        'enter_count_hotels': {
            'message': 'Сколько найти отелей?',
            'keyboard': {'type': 'reply', 'answers': [str(x) for x in range(2, 6)]},
            'next_step': 'need_photo'
        },
        'need_photo': {
            'message': 'Фото отелей прикрепить?',
            'keyboard': {'type': 'reply', 'answers': ['Да', 'Нет']},
            'next_step': ['enter_count_photo', 'finish']
        },
        'enter_count_photo': {
            'message': 'Сколько фото прикрепить?',
            'keyboard': {'type': 'reply', 'answers': [str(x) for x in range(4, 11, 2)]},
            'next_step': 'finish'
        },
    }

    def __init__(self):
        self.step = self.SCENARIO['start_step']
        self.hotel_api = SearchHotels()
        self.data = {}

    def start(self):
        return self._get_answer()

    def run(self, text: str):
        """
        Обрабатываем ответы пользователя и двигаемся по сценарию
        :param text: сообщение от пользователя
        :return: словарь с ответом от обработчика {'step': <name_step>, 'message_text': <text>, 'keyboard': <type>},
        но если step = 'finish' {'step': 'finish', 'hotels': []}
        """
        handler = getattr(self, '_' + self.step)  # Выбираем обработчик сообщения от пользователя (param = text)

        try:
            result = handler(text)  # return switch = (None or int) or error
        except ValueError as exc:
            return {
                'step': self.step,
                'message_text': exc,
                'keyboard': self.SCENARIO[self.step]['keyboard']
            }
        except (ConnectionError, HTTPError):
            return {
                'step': self.step,
                'message_text': 'Ошибка соединения с сервером...\nВыполни /reset и повтори запрос позже.',
                'keyboard': self.SCENARIO[self.step]['keyboard']
            }

        self._set_next_step(switch=result)
        if self.step == 'finish':
            return self._get_result_cmd()
        else:
            return self._get_answer()

    def _set_next_step(self, switch):
        if switch is None:
            self.step = self.SCENARIO[self.step]['next_step']
        else:
            self.step = self.SCENARIO[self.step]['next_step'][switch]

    def _get_answer(self):
        return {
            'step': self.step,
            'message_text': self.SCENARIO[self.step]['message'],
            'keyboard': self.SCENARIO[self.step]['keyboard']
        }

    #  Обработчики сообщений
    def _enter_city(self, text: str):
        result = self.hotel_api.search_city(location=text)
        self.data[self.step] = {'destinationID': result['destinationID'], 'city_name': result['city_name']}
        return None

    def _enter_date_from(self, text: str):
        if re.search(PATTERN_DATE, text):
            self.data[self.step] = text
            return None
        else:
            raise ValueError('Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')

    def _enter_date_to(self, text: str):
        if re.search(PATTERN_DATE, text):
            self.data[self.step] = text
            return None
        else:
            raise ValueError('Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')

    def _enter_count_hotels(self, text: str):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            return None
        else:
            raise ValueError('Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')

    def _need_photo(self, text: str):
        if text.lower() == 'да':
            self.data[self.step] = text
            return 0
        elif text.lower() == 'нет':
            self.data[self.step] = text
            return 1
        else:
            raise ValueError('Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')

    def _enter_count_photo(self, text: str):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            return None
        else:
            raise ValueError('Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')

    def _get_result_cmd(self):
        destination_id = self.data['enter_city']['destinationID']
        count_hotels = self.data['enter_count_hotels']
        check_in = self.data['enter_date_from']
        check_out = self.data['enter_date_to']

        hotels = self.hotel_api.search_hotels(destination_id, count_hotels, check_in, check_out)

        if self.data['need_photo'].lower() == 'да':
            count_photos = int(self.data['enter_count_photo'])

            for i, hotel in enumerate(hotels):
                url_photos = self.hotel_api.get_url_photos(hotel['id'], count_photos)
                hotels[i]['url_photos'] = url_photos

        return {'step': 'finish', 'hotels': hotels}
