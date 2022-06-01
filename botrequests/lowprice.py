import re


class CmdLowprice:

    COMMAND_NAME = 'lowprice'
    SCENARIO = {
        'start_step': 'enter_city',
        'enter_city': {'msg': 'Введите наименование города.', 'next_step': 'enter_date_from'},
        'enter_date_from': {'msg': 'Введите дату заезда.', 'next_step': 'enter_date_to'},
        'enter_date_to': {'msg': 'Введите дату отъезда.', 'next_step': 'enter_count_hotels'},
        'enter_count_hotels': {'msg': 'Введите количество отелей (не более 5-и).', 'next_step': 'need_photo'},
        'need_photo': {'msg': 'Выводить фото отелей?', 'next_step': ['enter_count_photo', 'get_results']},
        'enter_count_photo': {'msg': 'Количество фото отелей?', 'next_step': 'get_results'},
        'get_results': {'msg': 'Введи что то для результата', 'next_step': None},
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

        if self.step:
            return reply_msg
        else:
            return None

    def enter_city(self, text: str):
        if len(text) >= 3:
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step']
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильно ввели город. Попробуй снова.'

    def enter_date_from(self, text: str):
        pattern_date = r'^([1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|)20[0-9][0-9]$'
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
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильно ввели количество фото. Попробуй снова.'

    def get_results(self, text):
        if text.isdigit() and (1 <= int(text) <= 10):
            self.data[self.step] = text
            self.step = self.SCENARIO[self.step]['next_step']
            return self.SCENARIO[self.step]['msg']
        else:
            return 'Неправильно ввели количество фото. Попробуй снова.'













