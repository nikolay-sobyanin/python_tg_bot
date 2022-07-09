from telebot.types import Message
from loader import bot
from utils.logging.logger import my_logger


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    msg_text = 'Я помогаю найти отели.\n Ознакомься с моими командами /help'
    bot.send_message(message.from_user.id, msg_text)
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Отправил боту сообщение не находясь в сценарии команды.')
