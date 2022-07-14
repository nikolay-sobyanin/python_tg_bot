from loader import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar
from utils.misc.date_worker import DateWorker


class InlineMarkup:

    @staticmethod
    def create_callback_buttons(data: list) -> InlineKeyboardMarkup:
        """

        :param data: list of tuple(text, callback_data)
        :return:
        """
        markup = InlineKeyboardMarkup()
        for text, callback_data in data:
            markup.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        return markup

    @staticmethod
    def create_url_buttons(data: list) -> InlineKeyboardMarkup:
        """

        :param data: list of tuple(text, url)
        :return:
        """
        markup = InlineKeyboardMarkup()
        for text, url in data:
            markup.add(InlineKeyboardButton(text=text, url=url))
        return markup


class InlineCalendar:
    MIN_DATE = DateWorker.today()
    MAX_DATE = DateWorker.date_delta(days_delta=180)

    @staticmethod
    def create(message: Message or CallbackQuery, min_date=MIN_DATE, max_date=MAX_DATE) -> None:
        calendar, step = DetailedTelegramCalendar(min_date=min_date,
                                                  max_date=max_date, locale='ru').build()
        bot.send_message(message.from_user.id, f'Выбери:', reply_markup=calendar)

    @staticmethod
    def is_callback():
        return DetailedTelegramCalendar.func()

    @staticmethod
    def next_step(call: CallbackQuery, min_date=MIN_DATE, max_date=MAX_DATE) -> str or None:
        enter_date, key, step = DetailedTelegramCalendar(min_date=min_date,
                                                         max_date=max_date, locale='ru').process(call.data)
        if not enter_date and key:
            bot.edit_message_text(f'Выбери:', call.message.chat.id, call.message.message_id, reply_markup=key)
            return None
        else:
            bot.edit_message_text(f'Ты выбрал дату: {DateWorker.date_str(enter_date, "%d.%m.%Y")}',
                                  call.message.chat.id,
                                  call.message.message_id)
            return DateWorker.date_str(enter_date)

