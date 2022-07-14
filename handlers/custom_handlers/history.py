from loader import bot
from states.history import UserHistoryState
from telebot.types import Message, ReplyKeyboardRemove
from keyboards import reply_old
from database import db_worker
from utils.misc import date_worker
from utils.logging.logger import my_logger


@bot.message_handler(commands=['history'])
def bot_history(message: Message) -> None:
    bot.set_state(message.from_user.id, UserHistoryState.count_rows, message.chat.id)
    msg_text = 'Сколько вывести запросов команд?'
    markup = reply_old.reply_answers.get_markup([str(i) for i in range(2, 6)])
    bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
    my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                   f'Запустил команду бота /history.')


@bot.message_handler(state=UserHistoryState.count_rows)
def send_history(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 5):
        count_rows = int(message.text)
        history = db_worker.get_user_history(message.from_user.id, count_rows)
        for row in history:
            hotels = row["hotels"].replace(";", "\n")
            msg_text = f'Команда: {row["name_cmd"]}\n' \
                       f'Дата и время выполнения: {date_worker.get_date_time_str(row["time_cmd"])}\n' \
                       f'Найденные отели:\n' \
                       f'{hotels}'
            bot.send_message(message.from_user.id, msg_text)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.from_user.id, 'Я вывел историю запросов.', reply_markup=ReplyKeyboardRemove())
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Бот выполнил команду /history.')
    else:
        error_text = 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!'
        bot.send_message(message.from_user.id, error_text)
        my_logger.info(f'user id: {message.from_user.id}, user name: {message.from_user.full_name}. '
                       f'Неверный ввод количества истории запроса команд.')

