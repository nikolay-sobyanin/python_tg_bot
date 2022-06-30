from telebot.handler_backends import State, StatesGroup


class UserLowpriceState(StatesGroup):
    city = State()
    check_in = State()
    check_out = State()
    count_hotels = State()
    need_photos = State()
    count_photos = State()
