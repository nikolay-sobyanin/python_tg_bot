from loader import bot
from states.bestdeal import UserBestdealState
from telebot.types import Message, CallbackQuery
from utils.user_data_manager import UserData
from utils.commands_builder import FindCity, CheckIn, CheckOut, CountHotels, NeedPhotos, CountPhotos, FindHotels, \
    PriceRange, DistanceRange
from utils.logging.logger import my_logger

'''
Сценарий работы команды:
1) Поиск города: сообщение с запросом -> обработка ответа, уточнение поиска -> сохраняем в состояние инфу о городе
2) Ввод Check In, Check Out и сохраняем в состояние инфу
3) Ввод диапазона цен
4) Ввод диапазона расстояний
5) Ввод количества отелей
6) Ввод необходимости фото.
7) Если нужны запрос количества фото, иначе результат поиска.

Сохраняем в UserMemory
{
'command': <str>
'city': {'name': <str>, 'destination_id': <int>, 'coordinate': (<latitude_float> , <longitude_float>)},
'check_in': <str>,
'check_out': <str>,
'price_range': (<min_price_str>, <max_price_str>),
'distance_range': (<min_dist_str>, <max_dist_str>),
'count_hotels': <int>,
'need_photos': <str>,
#  Если key=need_photos, value='Да'
'count_photos': <int>, 
}
'''


@bot.message_handler(commands=['bestdeal'])
def bot_bestdeal(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Начнем поиск отелей подходящих по цене и расстоянию от центра.')

    bot.set_state(message.from_user.id, UserBestdealState.city, message.chat.id)
    UserData.set(message, 'command', message.text)
    my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Запустил {message.text}.')

    FindCity.start(message)


@bot.message_handler(state=UserBestdealState.city)
def city(message: Message) -> None:
    FindCity.find(message)


@bot.callback_query_handler(state=UserBestdealState.city, func=None)
def callback_city(call: CallbackQuery) -> None:
    if FindCity.catch(call):
        bot.set_state(call.from_user.id, UserBestdealState.check_in, call.message.chat.id)
        check_in(call)


@bot.message_handler(state=UserBestdealState.check_in)
def check_in(message: Message or CallbackQuery) -> None:
    CheckIn.start(message)


@bot.callback_query_handler(state=UserBestdealState.check_in, func=CheckIn.is_callback())
def callback_check_in(call: CallbackQuery) -> None:
    if CheckIn.catch(call):
        bot.set_state(call.from_user.id, UserBestdealState.check_out, call.message.chat.id)
        check_out(call)


@bot.message_handler(state=UserBestdealState.check_out)
def check_out(message: Message or CallbackQuery) -> None:
    CheckOut.start(message)


@bot.callback_query_handler(state=UserBestdealState.check_out, func=CheckOut.is_callback())
def callback_check_out(call: CallbackQuery) -> None:
    if CheckOut.catch(call):
        bot.set_state(call.from_user.id, UserBestdealState.price_range, call.message.chat.id)

        PriceRange.start(call)


@bot.message_handler(state=UserBestdealState.price_range)
def price_range(message: Message) -> None:
    if PriceRange.catch(message):
        bot.set_state(message.from_user.id, UserBestdealState.distance_range, message.chat.id)

        DistanceRange.start(message)


@bot.message_handler(state=UserBestdealState.distance_range)
def distance_range(message: Message) -> None:
    if DistanceRange.catch(message):
        bot.set_state(message.from_user.id, UserBestdealState.count_hotels, message.chat.id)

        CountHotels.start(message)


@bot.message_handler(state=UserBestdealState.count_hotels)
def count_hotels(message: Message) -> None:
    if CountHotels.catch(message):
        bot.set_state(message.from_user.id, UserBestdealState.need_photos, message.chat.id)

        NeedPhotos.start(message)


@bot.message_handler(state=UserBestdealState.need_photos)
def need_photos(message: Message) -> None:
    if NeedPhotos.catch(message):
        is_photos = UserData.get_one_value(message, 'need_photos')
        if is_photos.lower() == 'да':
            bot.set_state(message.from_user.id, UserBestdealState.count_photos, message.chat.id)

            CountPhotos.start(message)
        else:
            FindHotels.result(message)
            bot.delete_state(message.from_user.id, message.chat.id)
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Команда /bestdeal закончена.')


@bot.message_handler(state=UserBestdealState.count_photos)
def count_photos(message: Message) -> None:
    if CountPhotos.catch(message):
        FindHotels.result(message)
        bot.delete_state(message.from_user.id, message.chat.id)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Команда /bestdeal закончена.')
