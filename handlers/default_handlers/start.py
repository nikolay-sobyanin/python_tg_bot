from telebot.types import Message
from loader import bot
from utils.logging.logger import my_logger


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.full_name}!")
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Выполнил команду бота /start.')
