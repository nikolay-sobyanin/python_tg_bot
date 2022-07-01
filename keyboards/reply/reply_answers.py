from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_reply_answers_keyboard(answers: list) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for answer in answers:
        markup.add(answer)
    return markup


