from loader import bot
from telebot.types import Message
from utils.parsers import parser_cities
from keyboards import inline
from requests.exceptions import HTTPError, ConnectionError


def send_results(message: Message):
    msg_text = 'Подожди, ищу города...'
    bot.send_message(message.from_user.id, msg_text)

    try:
        cities = parser_cities.find_cities(message.text)
    except (HTTPError, ConnectionError) as exc:
        msg_text = str(exc)
        bot.send_message(message.from_user.id, msg_text)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id, message.chat.id)
    except ValueError as exc:
        msg_text = str(exc)
        bot.send_message(message.from_user.id, msg_text)
    else:
        markup = inline.cities.get_markup(cities)
        msg_text = 'Уточни, пожалуйста:'
        bot.send_message(message.from_user.id, msg_text, reply_markup=markup)

