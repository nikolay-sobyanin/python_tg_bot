from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS
from utils.logging.logger import my_logger


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    msg_text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    msg_text = f'Привет, {message.from_user.full_name}!\nМои команды:\n' + '\n'.join(msg_text)
    bot.send_message(message.from_user.id, msg_text)
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Выполнил команду бота /start.')
