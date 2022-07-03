from loader import bot
from telebot.types import Message
from config_data.config import FORMAT_DATE
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, datetime, timedelta


MIN_DATE = date.today()
MAX_DATE = date.today() + timedelta(days=180)


def send_calendar(message: Message, calendar_id: int, min_date=MIN_DATE, max_date=MAX_DATE):
    calendar, step = DetailedTelegramCalendar(calendar_id=calendar_id, min_date=min_date,
                                              max_date=max_date, locale='ru').build()
    bot.send_message(message.from_user.id, f'Выберите {step}', reply_markup=calendar)


def callback_calendar(calendar_id: int):
    return DetailedTelegramCalendar.func(calendar_id=calendar_id)


def next_step_calendar(call, calendar_id: int, min_date=MIN_DATE, max_date=MAX_DATE):
    enter_date, key, step = DetailedTelegramCalendar(calendar_id=calendar_id, min_date=min_date,
                                                     max_date=max_date, locale='ru').process(call.data)
    if not enter_date and key:
        bot.edit_message_text(f'Выбери {LSTEP[step]}', call.message.chat.id, call.message.message_id,
                              reply_markup=key)
        return None
    else:
        bot.edit_message_text(f'Ты выбрал дату: {enter_date.strftime("%d.%m.%Y")}',
                              call.message.chat.id,
                              call.message.message_id)
        return enter_date.strftime(FORMAT_DATE)


def get_date(date_str: str):
    return datetime.strptime(date_str, FORMAT_DATE).date()
