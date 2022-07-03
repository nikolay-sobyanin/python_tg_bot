from loader import bot
from telebot.types import Message
from config_data.config import FORMAT_DATE
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime


def send_calendar(message: Message, calendar_id: int, min_date=None, max_date=None):
    calendar, step = DetailedTelegramCalendar(calendar_id=calendar_id, min_date=min_date, max_date=max_date).build()
    bot.send_message(message.from_user.id, f'Выберите {step}', reply_markup=calendar)


def callback_calendar(calendar_id: int):
    return DetailedTelegramCalendar.func(calendar_id=calendar_id)


def next_step_calendar(call, calendar_id: int, min_date=None, max_date=None):
    enter_date, key, step = DetailedTelegramCalendar(calendar_id=calendar_id,
                                                     min_date=min_date, max_date=max_date).process(call.data)
    if not enter_date and key:
        bot.edit_message_text(f'Выбери {LSTEP[step]}', call.message.chat.id, call.message.message_id,
                              reply_markup=key)
        return None
    else:
        bot.edit_message_text(f'Ты выбрал дату: {enter_date.strftime("%d.%m.%Y")}',
                              call.message.chat.id,
                              call.message.message_id)
        return enter_date.strftime(FORMAT_DATE)
