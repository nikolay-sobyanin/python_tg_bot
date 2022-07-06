from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    msg_text = 'Я помогаю найти отели.\n Ознакомься с моими командами /help'
    bot.send_message(message.from_user.id, msg_text)
