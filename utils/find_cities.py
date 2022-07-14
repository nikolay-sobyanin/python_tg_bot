from loader import bot
from telebot.types import Message
from utils.parsers import parser_cities
from keyboards import inline_old
from requests.exceptions import HTTPError, ConnectionError
from utils.logging.logger import my_logger


def get_send_results(message: Message):
    msg_text = 'Подожди, ищу города...'
    bot.send_message(message.from_user.id, msg_text)

    try:
        cities = parser_cities.find_cities(message.text)
    except (HTTPError, ConnectionError) as exc:
        msg_text = str(exc)
        bot.send_message(message.from_user.id, msg_text)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
        my_logger.error(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                        f'Ошибка соединения с сервером.')
    except ValueError as exc:
        msg_text = str(exc)
        bot.send_message(message.from_user.id, msg_text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Бот не нашел города. Уточнение запроса от пользователя.')
    else:
        markup = inline_old.cities.get_markup(cities)
        msg_text = 'Уточни, пожалуйста:'
        bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
        return cities


