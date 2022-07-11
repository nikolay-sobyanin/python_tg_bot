from loader import bot
from telebot.types import Message, CallbackQuery


def set_data(message: Message or CallbackQuery, key: str, value) -> None:
    if isinstance(message, Message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data[key] = value
    elif isinstance(message, CallbackQuery):
        with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
            data[key] = value


def get_one_value(message: Message or CallbackQuery, key: str) -> str:
    if isinstance(message, Message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            return data[key]
    elif isinstance(message, CallbackQuery):
        with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
            return data[key]


def get_all_value(message: Message or CallbackQuery) -> dict:
    if isinstance(message, Message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            return data
    elif isinstance(message, CallbackQuery):
        with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
            return data
