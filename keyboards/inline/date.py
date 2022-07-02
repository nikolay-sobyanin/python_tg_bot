from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


def get_markup(calendar_id: int):
    calendar, step = DetailedTelegramCalendar(calendar_id=calendar_id).build()
    return calendar, LSTEP[step]
