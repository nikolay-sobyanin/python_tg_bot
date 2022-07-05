from telebot.types import Message
from loader import bot


@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice',
                                    'location', 'contact'])
def block_message(message: Message) -> None:
    msg_text = f'Прости, я не такой умный :(\nЯ понимаю только текс, но я буду учиться :)'
    bot.send_message(message.from_user.id, msg_text)





