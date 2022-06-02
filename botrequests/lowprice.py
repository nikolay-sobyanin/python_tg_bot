import re


class CmdLowprice:
    COMMAND_NAME = 'lowprice'
    SCENARIO = {
        'start_step': 'enter_city',
        'enter_city': {
            'message': 'В каком городе искать отели?\nБудь внимателен не ошибись!',
            'message_error': 'Что-то пошло не так...\nГород не найден, давай попробуем еще раз!',
            'keyboard_answer': {'type': 'standard'},
            'next_step': 'enter_date_from'
        },
        'enter_date_from': {
            'message': 'Когда заезжаем в отель?',
            'message_error': 'Что-то пошло не так...\nДата выбрана неверно, давай попробуем еще раз!',
            'keyboard_answer': {'type': 'date'},
            'next_step': 'enter_date_to'
        },
        'enter_date_to': {
            'message': 'Когда выезжаем из отеля?',
            'message_error': 'Что-то пошло не так...\nДата выбрана неверно, давай попробуем еще раз!',
            'keyboard_answer': {'type': 'date'},
            'next_step': 'enter_count_hotels'
        },
        'enter_count_hotels': {
            'message': 'Сколько вывести отелей?',
            'message_error': 'Что-то пошло не так...\nНеверный формат ввода, давай попробуем еще раз!',
            'keyboard_answer': {'type': 'reply', 'answers': [1, 2, 3, 4, 5]},
            'next_step': 'need_photo'
        },
        'need_photo': {
            'message': 'Фото отелей нужны?',
            'message_error': 'Что-то пошло не так...\nНеверный формат ввода, давай попробуем еще раз!',
            'keyboard_answer': {'type': 'reply', 'answers': ['Да', 'Нет']},
            'next_step': ['enter_count_photo', 'finish']
        },
        'enter_count_photo': {'msg': 'Количество фото отелей?', 'next_step': 'finish'},
    }

    def __init__(self):
        self.step = self.SCENARIO['start_step']
        self.data = {}

    def start(self):
        return self.SCENARIO[self.step]['message']

    def run(self, message):
        text = message.text
        handler = getattr(self, self.step)

        if type(self.SCENARIO[self.step]['next_step']) is list:
            if handler(text) is False:
                return self.SCENARIO[self.step]['message_error']

            switch = handler(text)
            self.step = self.SCENARIO[self.step]['next_step'][switch]
            if self.step == 'finish':
                return 'Мы закончили'
            return self.SCENARIO[self.step]['message']

        if handler(text):
            self.step = self.SCENARIO[self.step]['next_step']
            if self.step == 'finish':
                return 'Мы закончили'
            return self.SCENARIO[self.step]['message']
        else:
            return self.SCENARIO[self.step]['message_error']

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
