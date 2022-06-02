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
        return self.SCENARIO[self.step]['msg']

    def run(self, message):
        text = message.text
        handler = getattr(self, self.step)
        reply_msg = handler(text)

        return reply_msg

    def enter_city(self, text: str):
        if len(text) >= 3:
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step']
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильно ввели город. Попробуй снова.'

    def enter_date_from(self, text: str):
        pattern_date = r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'
        match = re.search(pattern_date, text)
        if match:
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step']
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильно ввели дату. Попробуй снова.'

    def enter_date_to(self, text: str):
        pattern_date = r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'
        match = re.search(pattern_date, text)
        if match:
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step']
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильно ввели дату. Попробуй снова.'

    def enter_count_hotels(self, text):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step']
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильно ввели количество отелей. Попробуй снова.'

    def need_photo(self, text):
        if text.lower() in ['yes', 'да']:
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step'][0]
            return self.SCENARIO[self.step]['msg']
        elif text.lower() in ['no', 'нет']:
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step'][1]
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильный ввод. Попробуй снова.'

    def enter_count_photo(self, text):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step']
            if self.step == 'finish':
                return 'Конец сценария'
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильно ввели количество фото. Попробуй снова.'
