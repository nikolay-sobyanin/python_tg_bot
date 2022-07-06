from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['reset'])
def bot_reset(message: Message) -> None:
    if bot.get_state(message.from_user.id, message.chat.id) is None:
        msg_text = f'Ты не выполняешь команду.'
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        msg_text = f'Команда сброшена.'

    bot.send_message(message.from_user.id, msg_text)
