from loader import bot
from telebot.types import Message, CallbackQuery


class UserData:

    @staticmethod
    def set(message: Message or CallbackQuery, key: str, value):
        if isinstance(message, Message):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data[key] = value
        elif isinstance(message, CallbackQuery):
            with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
                data[key] = value

    @staticmethod
    def get_one_value(message: Message or CallbackQuery, key: str):
        if isinstance(message, Message):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                return data[key]
        elif isinstance(message, CallbackQuery):
            with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
                return data[key]

    @staticmethod
    def get_all_value(message: Message or CallbackQuery):
        if isinstance(message, Message):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                return data
        elif isinstance(message, CallbackQuery):
            with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
                return data

    @staticmethod
    def del_one_value(message: Message or CallbackQuery, key: str):
        if isinstance(message, Message):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                del data[key]
        elif isinstance(message, CallbackQuery):
            with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
                del data[key]

    @staticmethod
    def reset(message: Message or CallbackQuery):
        if isinstance(message, Message):
            bot.reset_data(message.from_user.id, message.chat.id)
        elif isinstance(message, CallbackQuery):
            bot.reset_data(message.from_user.id, message.message.chat.id)


