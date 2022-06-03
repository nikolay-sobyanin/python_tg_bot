import re


class CmdLowprice:
    COMMAND_NAME = 'lowprice'
    SCENARIO = {
        'start_step': 'enter_city',
        'enter_city': {
            'message': 'В каком городе искать отели?\nБудь внимателен не ошибись!',
            'message_error': 'Что-то пошло не так...\nГород не найден, давай попробуем еще раз!',
            'keyboard': {'type': None},
            'next_step': 'enter_date_from'
        },
        'enter_date_from': {
            'message': 'Когда заезжаем в отель?',
            'message_error': 'Что-то пошло не так...\nДата выбрана неверно, давай попробуем еще раз!',
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
            'message_error': 'Что-то пошло не так...\nНеверный формат ввода, давай попробуем еще раз!',
            'keyboard': {'type': 'reply', 'answers': [str(x) for x in range(1, 6)]},
            'next_step': 'need_photo'
        },
        'need_photo': {
            'message': 'Фото отелей нужны?',
            'message_error': 'Что-то пошло не так...\nНеверный формат ввода, давай попробуем еще раз!',
            'keyboard': {'type': 'reply', 'answers': ['Да', 'Нет']},
            'next_step': ['enter_count_photo', 'finish']
        },
        'enter_count_photo': {
            'message': 'Сколько фото отелей вывести?',
            'message_error': 'Что-то пошло не так...\nНеверный формат ввода, давай попробуем еще раз!',
            'keyboard': {'type': 'reply', 'answers': [str(x) for x in range(2, 11, 2)]},
            'next_step': 'finish'
        },
    }

    def __init__(self):
        self.step = self.SCENARIO['start_step']
        self.data = {}

    def start(self):
        return {
                'step': self.step,
                'message_text': self.SCENARIO[self.step]['message'],
                'keyboard': self.SCENARIO[self.step]['keyboard']
            }

    def run(self, message):
        text = message.text
        handler = getattr(self, self.step)
        result_handler = handler(text)

        if result_handler is False:
            return {
                'step': self.step,
                'message_text': self.SCENARIO[self.step]['message_error'],
                'keyboard': self.SCENARIO[self.step]['keyboard']
            }
        elif result_handler is True:
            self.step = self.SCENARIO[self.step]['next_step']
        elif isinstance(result_handler, int):
            switch = result_handler
            self.step = self.SCENARIO[self.step]['next_step'][switch]
        else:
            raise TypeError

        if self.step == 'finish':
            return {
                'step': self.step,
                'message_text': f'Команда {self.COMMAND_NAME} выполнена!',
                'keyboard': {'type': None},
            }
        else:
            return {
                'step': self.step,
                'message_text': self.SCENARIO[self.step]['message'],
                'keyboard': self.SCENARIO[self.step]['keyboard']
            }

    def enter_city(self, text: str):
        if len(text) >= 3:
            self.data[self.step] = text
            return True
        else:
            return False

    def enter_date_from(self, text: str):
        pattern_date = r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'
        match = re.search(pattern_date, text)
        if match:
            self.data[self.step] = text
            return True
        else:
            return False

    def enter_date_to(self, text: str):
        pattern_date = r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'
        match = re.search(pattern_date, text)
        if match:
            self.data[self.step] = text
            return True
        else:
            return False

    def enter_count_hotels(self, text):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            return True
        else:
            return False

    def need_photo(self, text):
        if text.lower() == 'да':
            self.data[self.step] = text
            switch = 0
            return switch
        elif text.lower() == 'нет':
            self.data[self.step] = text
            switch = 1
            return switch
        else:
            return False

    def enter_count_photo(self, text):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            return True
        else:
            return False
