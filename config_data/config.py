import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

#  HOTEL API
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
HOTELS_API_HOST = 'hotels4.p.rapidapi.com'
START_URL = 'https://hotels4.p.rapidapi.com'
HEADERS = {
    "X-RapidAPI-Host": HOTELS_API_HOST,
    "X-RapidAPI-Key": RAPID_API_KEY
}
LOCALE = 'en_US'
CURRENCY = 'USD'


DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', "Найду самые дешёвые отели в городе"),
)

PATTERN_DATE = r'^202\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$'
FORMAT_DATE = '%Y-%m-%d'
