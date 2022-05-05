DEFAULT_MESSAGE = 'ОШИБКА! Неверный запрос.\n\n/help - справка по работе с ботом'

DESCRIPTION = {
    'start': 'Выберите команду для поиска:\n'
             '/help - справка по командам\n'
             '/lowprice - поиск самых дешёвых отелей в городе\n'
             '/highprice - поиск самых дорогих отелей в городе\n'
             '/bestdeal — поиск отелей, наиболее подходящих по цене и расположению от центра\n'
             '/history — вывод истории поиска отелей',
    'help': 'Команда help',
    'lowprice': 'Команда lowprice',
    'highprice': 'Команда highprice',
    'bestdeal': 'Команда bestdeal',
    'history': 'Команда history',
}

COMMAND = {
    'start': {'scenario': None, 'answer': DESCRIPTION['start']},
    'help': {'scenario': None, 'answer': DESCRIPTION['help']},
    'lowprice': {'scenario': 'search_lowprice', 'answer': DESCRIPTION['lowprice']},
    'highprice': {'scenario': 'search_highprice', 'answer': DESCRIPTION['highprice']},
    'bestdeal': {'scenario': 'search_bestdeal', 'answer': DESCRIPTION['bestdeal']},
    'history': {'scenario': 'get_history', 'answer': DESCRIPTION['history']},
}
