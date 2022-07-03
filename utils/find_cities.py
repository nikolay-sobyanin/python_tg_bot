from loader import bot
from telebot.types import Message
from utils.parsers.parser_cities import find_cities
from keyboards import inline


def send_results(message: Message):
    cities = find_cities(message.text)
    markup = inline.cities.get_markup(cities)
    msg_text = 'Уточни, пожалуйста:'
    bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
