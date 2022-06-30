import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', "Найду самые дешёвые отели в городе"),
)

PATTERN_DATE = r'^202\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$'
FORMAT_DATE = '%Y-%m-%d'
