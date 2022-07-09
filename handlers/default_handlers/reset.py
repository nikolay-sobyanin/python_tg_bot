from telebot.types import Message
from loader import bot
from utils.logging.logger import my_logger


@bot.message_handler(commands=['reset'])
def bot_reset(message: Message) -> None:
    if bot.get_state(message.from_user.id, message.chat.id) is None:
        msg_text = f'Ты не выполняешь команду.'
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Выполнил команду бота /reset, но не выполнял другую команду.')
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        msg_text = f'Команда сброшена.'
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Выполнил команду бота /reset, сбросил выполнение команды.')

    bot.send_message(message.from_user.id, msg_text)
