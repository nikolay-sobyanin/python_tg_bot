from loader import bot
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar
from utils.misc import date_worker

MIN_DATE = date_worker.get_today()
MAX_DATE = date_worker.get_delta_date(days=180)


def send_calendar(message: Message or CallbackQuery, min_date=MIN_DATE, max_date=MAX_DATE):
    calendar, step = DetailedTelegramCalendar(min_date=min_date,
                                              max_date=max_date, locale='ru').build()
    bot.send_message(message.from_user.id, f'Выбери:', reply_markup=calendar)


def callback_calendar():
    return DetailedTelegramCalendar.func()


def next_step_calendar(call, min_date=MIN_DATE, max_date=MAX_DATE):
    enter_date, key, step = DetailedTelegramCalendar(min_date=min_date,
                                                     max_date=max_date, locale='ru').process(call.data)
    if not enter_date and key:
        bot.edit_message_text(f'Выбери:', call.message.chat.id, call.message.message_id,
                              reply_markup=key)
        return None
    else:
        bot.edit_message_text(f'Ты выбрал дату: {date_worker.get_date_str(enter_date, format_date="%d.%m.%Y")}',
                              call.message.chat.id,
                              call.message.message_id)
        return date_worker.get_date_str(enter_date)
