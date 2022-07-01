from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_inline_url_keyboard(text, url):
    markup = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text=text, url=url)
    markup.add(url_button)
    return markup
