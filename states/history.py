from telebot.handler_backends import State, StatesGroup


class UserHistoryState(StatesGroup):
    count_rows = State()
