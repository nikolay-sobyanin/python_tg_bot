from loader import bot
from states.highprice import UserHighpriceState
from telebot.types import Message, CallbackQuery
from utils.user_data_manager import UserData
from utils.commands_builder import FindCity, CheckIn, CheckOut, CountHotels, NeedPhotos, CountPhotos, FindHotels
from utils.logging.logger import my_logger


@bot.message_handler(commands=['highprice'])
def bot_lowprice(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Начнем поиск самых дешевых отелей.')

    bot.set_state(message.from_user.id, UserHighpriceState.city, message.chat.id)
    UserData.set(message, 'command', message.text)
    my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Запустил {message.text}.')

    FindCity.start(message)


@bot.message_handler(state=UserHighpriceState.city)
def city(message: Message) -> None:
    FindCity.find(message)


@bot.callback_query_handler(state=UserHighpriceState.city, func=None)
def callback_city(call: CallbackQuery) -> None:
    if FindCity.catch(call):
        bot.set_state(call.from_user.id, UserHighpriceState.check_in, call.message.chat.id)
        check_in(call)


@bot.message_handler(state=UserHighpriceState.check_in)
def check_in(message: Message or CallbackQuery) -> None:
    CheckIn.start(message)


@bot.callback_query_handler(state=UserHighpriceState.check_in, func=CheckIn.is_callback())
def callback_check_in(call: CallbackQuery) -> None:
    if CheckIn.catch(call):
        bot.set_state(call.from_user.id, UserHighpriceState.check_out, call.message.chat.id)
        check_out(call)


@bot.message_handler(state=UserHighpriceState.check_out)
def check_out(message: Message or CallbackQuery) -> None:
    CheckOut.start(message)


@bot.callback_query_handler(state=UserHighpriceState.check_out, func=CheckOut.is_callback())
def callback_calendar_check_out(call: CallbackQuery) -> None:
    if CheckOut.catch(call):
        bot.set_state(call.from_user.id, UserHighpriceState.count_hotels, call.message.chat.id)

        CountHotels.start(call)


@bot.message_handler(state=UserHighpriceState.count_hotels)
def count_hotels(message: Message) -> None:
    if CountHotels.catch(message):
        bot.set_state(message.from_user.id, UserHighpriceState.need_photos, message.chat.id)

        NeedPhotos.start(message)


@bot.message_handler(state=UserHighpriceState.need_photos)
def need_photos(message: Message) -> None:
    if NeedPhotos.catch(message):
        is_photos = UserData.get_one_value(message, 'need_photos')
        if is_photos.lower() == 'да':
            bot.set_state(message.from_user.id, UserHighpriceState.count_photos, message.chat.id)

            CountPhotos.start(message)
        else:
            FindHotels.result(message, sort_order='PRICE_HIGHEST_FIRST')
            bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=UserHighpriceState.count_photos)
def count_photos(message: Message) -> None:
    if CountPhotos.catch(message):
        FindHotels.result(message, sort_order='PRICE_HIGHEST_FIRST')
        bot.delete_state(message.from_user.id, message.chat.id)
