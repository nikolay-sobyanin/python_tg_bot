from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_markup(cities: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for city in cities:
        markup.add(InlineKeyboardButton(text=city['city_name'],
                                        callback_data=f'{city["destination_id"]}'))
    return markup
