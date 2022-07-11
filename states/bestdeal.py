from telebot.handler_backends import State, StatesGroup


class UserBestdealState(StatesGroup):
    city = State()
    check_in = State()
    check_out = State()
    price_range = State()
    distance_range = State()
    count_hotels = State()
    need_photos = State()
    count_photos = State()
