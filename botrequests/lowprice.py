class CmdLowprice:

    COMMAND_NAME = 'lowprice'
    SCENARIO = {
        'start_step': 'city',
        'city': {'msg': 'Введите наименование города.', 'next_step': 'date_from'},
        'date_from': {'msg': 'Введите дату заезда.', 'next_step': 'date_to'},
        'date_to': {'msg': 'Введите дату отъезда.', 'next_step': 'count_hotels'},
        'count_hotels': {'msg': 'Введите количество отелей (не более 5-и).', 'next_step': 'need_photo'},
        'need_photo': {'msg': 'Выводить фото отелей?', 'next_step': ['count_photo', 'get_results']},
        'count_photo': {'msg': 'Количество фото отелей?', 'next_step': 'get_results'},
        'get_results': {'msg': 'Введи что то для результата', 'next_step': None},
    }

    def __init__(self):
        self.step = None
        self.data = {
            'city': None,
            'date_from': None,
            'date_to': None,
            'count_hotels': None,
            'need_photo': None,
            'count_photos': None,
        }










