from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS
from utils.logging.logger import my_logger


@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice',
                                    'location', 'contact'])
def bot_block_message(message: Message) -> None:
    msg_text = f'Прости, я не такой умный :(\nЯ понимаю только текс, но я буду учиться :)'
    bot.send_message(message.from_user.id, msg_text)
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Отправил боту не текст.')


@bot.message_handler(commands=[i[0] for i in DEFAULT_COMMANDS if i[0] != 'reset'],
                     func=lambda message: False if bot.get_state(message.from_user.id, message.chat.id) is None
                     else True)
def bot_block_command(message: Message) -> None:
    msg_text = f'Ты выполняешь команду.\nДля сброса выполни /reset'
    bot.send_message(message.from_user.id, msg_text)
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Пытался вызвать другую команду находясь в сценарии другой.')
