import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
HOTELS_API_KEY = os.getenv('HOTELS_API_KEY')
PATH_DB = 'data_base/DB.db'

PATTERN_DATE = r'^202\d.(0[1-9]|1[012]).(0[1-9]|[12][0-9]|3[01])$'
FORMAT_DATE = '%Y-%m-%d'
