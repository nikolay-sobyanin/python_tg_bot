from loader import bot
from states.history import UserHistoryState
from telebot.types import Message, ReplyKeyboardRemove
from database.db_worker import DataBaseWorker
from utils.misc.date_worker import DateWorker
from keyboards.reply import ReplyMarkup
from utils.logging.logger import my_logger


@bot.message_handler(commands=['history'])
def bot_history(message: Message) -> None:
    markup = ReplyMarkup.create_many_button([str(i) for i in range(2, 6)])
    bot.send_message(message.from_user.id, 'Сколько вывести запросов команд?', reply_markup=markup)
    bot.set_state(message.from_user.id, UserHistoryState.count_rows, message.chat.id)
    my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Запустил {message.text}.')


@bot.message_handler(state=UserHistoryState.count_rows)
def send_history(message: Message) -> None:
    if message.text.isdigit() and (1 <= int(message.text) <= 5):
        count_rows = int(message.text)
        history = DataBaseWorker.get_user_history(message.from_user.id, count_rows)
        for row in history:
            hotels = row["hotels"].replace(";", "\n")
            msg_text = f'Команда: {row["name_cmd"]}\n' \
                       f'Дата и время выполнения: {DateWorker.date_time_str(row["time_cmd"])}\n' \
                       f'Найденные отели:\n' \
                       f'{hotels}'
            bot.send_message(message.from_user.id, msg_text)
        bot.send_message(message.from_user.id, 'Я вывел историю запросов.', reply_markup=ReplyKeyboardRemove())
        bot.delete_state(message.from_user.id, message.chat.id)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Закончил команду /history.')
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Неверный ввод')

