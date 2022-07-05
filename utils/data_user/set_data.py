from loader import bot
from telebot.types import Message, CallbackQuery


def execute(message: Message or CallbackQuery, key: str, value: str) -> None:
    if isinstance(message, Message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data[key] = value
    elif isinstance(message, CallbackQuery):
        with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
            data[key] = value
