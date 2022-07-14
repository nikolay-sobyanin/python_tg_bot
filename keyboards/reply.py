from telebot.types import ReplyKeyboardMarkup


class ReplyMarkup:

    @staticmethod
    def create_many_button(answers: list) -> ReplyKeyboardMarkup:
        """

        :param answers: answers for user
        :return:
        """
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for answer in answers:
            markup.add(answer)
        return markup
