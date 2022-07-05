from telebot.types import ReplyKeyboardMarkup


def get_markup(answers: list) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for answer in answers:
        markup.add(answer)
    return markup


