from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from utils.logging.logger import my_logger
import handlers  # Инициализация хендлеров


def main():
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    my_logger.info(f'{"ЗАПУСК БОТА":*^20}')
    bot.infinity_polling()


if __name__ == '__main__':
    main()
