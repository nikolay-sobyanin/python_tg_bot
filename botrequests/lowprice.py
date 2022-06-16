import re
from search_hotels import SearchHotels
from config import PATTERN_DATE


class CmdLowprice:
    COMMAND_NAME = 'lowprice'
    SCENARIO = {
        'start_step': 'enter_city',
        'enter_city': {
            'message': 'В каком городе искать отели?\nБудь внимателен не ошибись!',
            'keyboard': {'type': None},
            'next_step': 'enter_date_from'
        },
        'enter_date_from': {
            'message': 'Когда заезжаем в отель?',
            'keyboard': {'type': 'date'},
            'next_step': 'enter_date_to'
        },
        'enter_date_to': {
            'message': 'Когда выезжаем из отеля?',
            'message_error': 'Что-то пошло не так...\nДата выбрана неверно, давай попробуем еще раз!',
            'keyboard': {'type': 'date'},
            'next_step': 'enter_count_hotels'
        },
        'enter_count_hotels': {
            'message': 'Сколько вывести отелей?',
            'keyboard': {'type': 'reply', 'answers': [str(x) for x in range(2, 6)]},
            'next_step': 'need_photo'
        },
        'need_photo': {
            'message': 'Фото отелей нужны?',
            'keyboard': {'type': 'reply', 'answers': ['Да', 'Нет']},
            'next_step': ['enter_count_photo', 'finish']
        },
        'enter_count_photo': {
            'message': 'Сколько фото отелей вывести?',
            'keyboard': {'type': 'reply', 'answers': [str(x) for x in range(4, 11, 2)]},
            'next_step': 'finish'
        },
    }

    def __init__(self):
        self.step = self.SCENARIO['start_step']
        self.hotel_api = SearchHotels()
        self.data = {}

    def start(self):
        """
        Выдаем сообщение для стартового шага
        :return: возвращаем словарь с параметрами ответа
        """
        return {
                'step': self.step,
                'message_text': self.SCENARIO[self.step]['message'],
                'keyboard': self.SCENARIO[self.step]['keyboard']
            }

    def run(self, text: str):
        """
        Обрабатываем ответы пользователя и двигаемся по сценарию
        :param text: сообщение от пользователя
        :return: dict с результатом сценария или шага
        """
        handler = getattr(self, '_' + self.step)
        result_handler = handler(text)
        if result_handler['set_next_step']:
            self._set_next_step(switch=result_handler['switch'])
            return self._get_answer()
        else:
            return self._get_error(text_error=result_handler['text_error'])

    def _set_next_step(self, switch):
        if switch is None:
            self.step = self.SCENARIO[self.step]['next_step']
        elif isinstance(switch, int) and 0 <= switch <= len(self.SCENARIO[self.step]['next_step']) - 1:
            self.step = self.SCENARIO[self.step]['next_step'][switch]
        else:
            raise TypeError

    def _get_answer(self):
        if self.step == 'finish':
            return self._get_result_cmd()
        else:
            return {
                'step': self.step,
                'message_text': self.SCENARIO[self.step]['message'],
                'keyboard': self.SCENARIO[self.step]['keyboard']
            }

    def _get_error(self, text_error: str):
        return {
            'step': self.step,
            'message_text': text_error,
            'keyboard': self.SCENARIO[self.step]['keyboard']
        }

    #  Обработчики сообщений
    def _create_result(self, set_next_step: bool, switch=None, text_error=None):
        return {
            'set_next_step': set_next_step,
            'switch': switch,
            'text_error': text_error
        }

    def _enter_city(self, text: str):
        result = self.hotel_api.search_city(location=text)
        if result['city_found']:
            self.data[self.step] = {'destinationID': result['destinationID'], 'city_name': result['city_name']}
            return self._create_result(set_next_step=True)
        else:
            return self._create_result(set_next_step=False, text_error=result['text_error'])

    def _enter_date_from(self, text: str):
        if re.search(PATTERN_DATE, text):
            self.data[self.step] = text
            return self._create_result(set_next_step=True)
        else:
            text_error = 'Что-то пошло не так...\nДата выбрана неверно, давай попробуем еще раз!'
            return self._create_result(set_next_step=False, text_error=text_error)

    def _enter_date_to(self, text: str):
        if re.search(PATTERN_DATE, text):
            self.data[self.step] = text
            return self._create_result(set_next_step=True)
        else:
            text_error = 'Что-то пошло не так...\nДата выбрана неверно, давай попробуем еще раз!'
            return self._create_result(set_next_step=False, text_error=text_error)

    def _enter_count_hotels(self, text: str):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            return self._create_result(set_next_step=True)
        else:
            text_error = 'Что-то пошло не так...\nНеверный формат ввода, давай попробуем еще раз!'
            return self._create_result(set_next_step=False, text_error=text_error)

    def _need_photo(self, text: str):
        if text.lower() == 'да':
            self.data[self.step] = text
            switch = 0
            return self._create_result(set_next_step=True, switch=switch)
        elif text.lower() == 'нет':
            self.data[self.step] = text
            switch = 1
            return self._create_result(set_next_step=True, switch=switch)
        else:
            text_error = 'Что-то пошло не так...\nНеверный формат ввода, давай попробуем еще раз!'
            return self._create_result(set_next_step=False, text_error=text_error)

    def _enter_count_photo(self, text: str):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            return self._create_result(set_next_step=True)
        else:
            text_error = 'Что-то пошло не так...\nНеверный формат ввода, давай попробуем еще раз!'
            return self._create_result(set_next_step=False, text_error=text_error)

    def _get_result_cmd(self):
        destination_id = self.data['enter_city']['destinationID']
        count_hotels = self.data['enter_count_hotels']
        check_in = self.data['enter_date_from']
        check_out = self.data['enter_date_to']

        data_hotels = self.hotel_api.search_hotels(destination_id, count_hotels, check_in, check_out)

        if data_hotels['hotels_found']:
            if self.data['need_photo'] == 'да':
                count_photos = int(self.data['enter_count_photo'])

                for hotel in data_hotels['hotels']:
                    url_photos = self.hotel_api.get_url_photos(hotel['id'], count_photos)
                    hotel['url_photos'] = url_photos['urls']

        return {'step': 'finish', 'data_hotels': data_hotels}



