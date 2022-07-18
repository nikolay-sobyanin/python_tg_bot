from loader import bot
from states.lowprice import UserLowpriceState
from telebot.types import Message, CallbackQuery
from utils.user_data_manager import UserData
from utils.commands_builder import FindCity, CheckIn, CheckOut, CountHotels, NeedPhotos, CountPhotos, FindHotels
from utils.logging.logger import my_logger

'''
Сценарий работы команды:
1) Поиск города: сообщение с запросом -> обработка ответа, уточнение поиска -> сохраняем в состояние инфу о городе
2) Ввод Check In, Check Out и сохраняем в состояние инфу
3) Ввод количества отелей
4) Ввод необходимости фото.
5) Если нужны запрос количества фото, иначе результат поиска.

Сохраняем в UserMemory
{
'command': <str>
'city': {'name': <str>, 'destination_id': <int>, 'coordinate': (<latitude_float> , <longitude_float>)},
'check_in': <str>,
'check_out': <str>,
'count_hotels': <int>,
'need_photos': <str>,
#  Если key=need_photos, value='Да'
'count_photos': <int>, 
}
'''


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Начнем поиск самых дешевых отелей.')

    bot.set_state(message.from_user.id, UserLowpriceState.city, message.chat.id)
    UserData.set(message, 'command', message.text)
    my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Запустил {message.text}.')

    FindCity.start(message)


@bot.message_handler(state=UserLowpriceState.city)
def city(message: Message) -> None:
    FindCity.find(message)


@bot.callback_query_handler(state=UserLowpriceState.city, func=None)
def callback_city(call: CallbackQuery) -> None:
    if FindCity.catch(call):
        bot.set_state(call.from_user.id, UserLowpriceState.check_in, call.message.chat.id)
        check_in(call)


@bot.message_handler(state=UserLowpriceState.check_in)
def check_in(message: Message or CallbackQuery) -> None:
    CheckIn.start(message)


@bot.callback_query_handler(state=UserLowpriceState.check_in, func=CheckIn.is_callback())
def callback_check_in(call: CallbackQuery) -> None:
    if CheckIn.catch(call):
        bot.set_state(call.from_user.id, UserLowpriceState.check_out, call.message.chat.id)
        check_out(call)


@bot.message_handler(state=UserLowpriceState.check_out)
def check_out(message: Message or CallbackQuery) -> None:
    CheckOut.start(message)


@bot.callback_query_handler(state=UserLowpriceState.check_out, func=CheckOut.is_callback())
def callback_check_out(call: CallbackQuery) -> None:
    if CheckOut.catch(call):
        bot.set_state(call.from_user.id, UserLowpriceState.count_hotels, call.message.chat.id)

        CountHotels.start(call)


@bot.message_handler(state=UserLowpriceState.count_hotels)
def count_hotels(message: Message) -> None:
    if CountHotels.catch(message):
        bot.set_state(message.from_user.id, UserLowpriceState.need_photos, message.chat.id)

        NeedPhotos.start(message)


@bot.message_handler(state=UserLowpriceState.need_photos)
def need_photos(message: Message) -> None:
    if NeedPhotos.catch(message):
        is_photos = UserData.get_one_value(message, 'need_photos')
        if is_photos.lower() == 'да':
            bot.set_state(message.from_user.id, UserLowpriceState.count_photos, message.chat.id)

            CountPhotos.start(message)
        else:
            FindHotels.result(message)
            bot.delete_state(message.from_user.id, message.chat.id)
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Команда /lowprice закончена.')


@bot.message_handler(state=UserLowpriceState.count_photos)
def count_photos(message: Message) -> None:
    if CountPhotos.catch(message):
        FindHotels.result(message)
        bot.delete_state(message.from_user.id, message.chat.id)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Команда /lowprice закончена.')
