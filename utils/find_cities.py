from loader import bot
from telebot.types import Message
from utils.parsers import parser_cities
from keyboards import inline


def send_results(message: Message):
    cities = parser_cities.find_cities(message.text)
    markup = inline.cities.get_markup(cities)
    msg_text = 'Уточни, пожалуйста:'
    bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
