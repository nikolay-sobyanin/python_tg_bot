from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from utils.logging.logger import my_logger


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    msg_text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(msg_text))
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Выполнил команду бота /help.')
