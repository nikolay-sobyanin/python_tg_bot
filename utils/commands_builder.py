import re
import json
from loader import bot
from telebot.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove
from .misc.api_hotels import APIHotels
from .misc.date_worker import DateWorker
from config_data.config import START_URL, HEADERS, LOCALE, CURRENCY
from requests.exceptions import HTTPError, ConnectionError
from keyboards.inline import InlineMarkup, InlineCalendar
from keyboards.reply import ReplyMarkup
from .user_data_manager import UserData
from database.db_worker import DataBaseWorker
from .logging.logger import my_logger
from geopy.distance import distance


class FindCity:

    @staticmethod
    def start(message: Message) -> None:
        msg_text = 'В каком городе искать отели?\n' \
                   'Чтобы мне было проще укажи страну, регион, город на английском языке.\n\n' \
                   'ВАЖНО! Временно поиск отелей в России недоступен.'
        bot.send_message(message.from_user.id, msg_text)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Начал поиск городов.')

    @staticmethod
    def _parser(city: str) -> list:
        url = START_URL + '/locations/v2/search'
        querystring = {'query': city, 'locale': LOCALE, 'currency': CURRENCY}
        data_text = APIHotels.request_api(url=url, headers=HEADERS, querystring=querystring)

        pattern = r'(?<="CITY_GROUP",).+?[\]]'
        find = re.search(pattern, data_text)
        if find:
            data_json = json.loads(f"{{{find[0]}}}")

            cities = list()
            for city in data_json['entities']:
                city_name = re.sub(r'</?span.*?>', '', city['caption'])
                cities.append({
                    'city_name': city_name,
                    'destination_id': city['destinationId'],
                    'city_coordinate': (city['latitude'], city['longitude'])
                })

            if not cities:
                raise ValueError('Я не нашел города.\nУточни запрос.')

            return cities
        else:
            raise HTTPError('Не могу обработать ответ от сервера...\nКоманда сброшена. Выполни запрос позже..')

    @staticmethod
    def find(message: Message) -> None:
        bot.send_message(message.from_user.id, 'Подожди, ищу города...')
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Запрос к API HOTELS.')
        try:
            cities = FindCity._parser(message.text)
        except (HTTPError, ConnectionError) as exc:
            bot.send_message(message.from_user.id, str(exc))
            bot.delete_state(message.from_user.id, message.chat.id)
            UserData.reset(message)
            my_logger.error(f'{message.from_user.full_name} (id: {message.from_user.id}): Ошибка на сервере.')
        except ValueError as exc:
            bot.send_message(message.from_user.id, str(exc))
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Города по запросу не найдены.')
        else:
            UserData.set(message, 'cities', cities)
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Сохранил города.')
            markup = InlineMarkup.create_callback_buttons(
                [(city['city_name'], city['destination_id']) for city in cities]
            )
            bot.send_message(message.from_user.id, 'Уточни, пожалуйста:', reply_markup=markup)
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Уточнение поиска города.')

    @staticmethod
    def catch(call: CallbackQuery) -> bool:
        destination_id = call.data

        cities = UserData.get_one_value(call, 'cities')
        for city in cities:
            if city['destination_id'] == destination_id:
                UserData.set(call, 'city', city)
                bot.edit_message_text(f'Ты выбрал город: {city["city_name"]}',
                                      call.message.chat.id, call.message.message_id)
                UserData.del_one_value(call, 'cities')
                my_logger.info(f'{call.from_user.full_name} (id: {call.from_user.id}): '
                               f'Выбрал город: {city["city_name"]}.')
                return True
        return False


class CheckIn:

    @staticmethod
    def start(message: Message or CallbackQuery):
        bot.send_message(message.from_user.id, 'Выбери дату заезда?')
        InlineCalendar.create(message)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Начал выбор check in.')

    @staticmethod
    def is_callback():
        return InlineCalendar.is_callback()

    @staticmethod
    def catch(call: CallbackQuery) -> bool:
        enter_date = InlineCalendar.next_step(call)
        if enter_date:
            UserData.set(call, 'check_in', enter_date)
            my_logger.info(f'{call.from_user.full_name} (id: {call.from_user.id}): Check in: {enter_date}.')
            return True
        return False


class CheckOut:

    @staticmethod
    def _min_date(message: Message or CallbackQuery):
        date_check_in = UserData.get_one_value(message, 'check_in')
        date_check_in = DateWorker.date_obj(date_check_in)
        return DateWorker.date_delta(days_delta=1, start_date=date_check_in)

    @staticmethod
    def start(message: Message or CallbackQuery):
        bot.send_message(message.from_user.id, 'Выбери дату отъезда?')
        InlineCalendar.create(message, min_date=CheckOut._min_date(message))
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Начал выбор check out.')

    @staticmethod
    def is_callback():
        return InlineCalendar.is_callback()

    @staticmethod
    def catch(call: CallbackQuery) -> bool:
        enter_date = InlineCalendar.next_step(call, min_date=CheckOut._min_date(call))
        if enter_date:
            UserData.set(call, 'check_out', enter_date)
            my_logger.info(f'{call.from_user.full_name} (id: {call.from_user.id}): Check out: {enter_date}.')
            return True
        return False


class CountHotels:

    @staticmethod
    def start(message: Message or CallbackQuery) -> None:
        markup = ReplyMarkup.create_many_button([str(i) for i in range(2, 6)])
        bot.send_message(message.from_user.id, 'Сколько найти отелей?', reply_markup=markup)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Начал выбор кол-во отелей.')

    @staticmethod
    def catch(message: Message) -> bool:
        if message.text.isdigit() and (1 <= int(message.text) <= 5):
            UserData.set(message, 'count_hotels', message.text)
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): '
                           f'Кол-во отелей: {message.text}.')
            return True
        else:
            bot.send_message(message.from_user.id, 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Неверный ввод')
            return False


class NeedPhotos:

    @staticmethod
    def start(message: Message or CallbackQuery) -> None:
        markup = ReplyMarkup.create_many_button(['Да', 'Нет'])
        bot.send_message(message.from_user.id, 'Фото отелей прикрепить?', reply_markup=markup)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Начал выбор необходимости фото.')

    @staticmethod
    def catch(message: Message) -> bool:
        if message.text.lower() in ['да', 'нет']:
            UserData.set(message, 'need_photos', message.text)
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): '
                           f'Необходимость фото: {message.text}.')
            return True
        else:
            bot.send_message(message.from_user.id, 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Неверный ввод')
            return False


class CountPhotos:

    @staticmethod
    def start(message: Message or CallbackQuery) -> None:
        markup = ReplyMarkup.create_many_button([str(i) for i in range(4, 11, 2)])
        bot.send_message(message.from_user.id, 'Сколько фото прикрепить?', reply_markup=markup)
        my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Начал выбор кол-во фото.')

    @staticmethod
    def catch(message: Message) -> bool:
        if message.text.isdigit() and (1 <= int(message.text) <= 10):
            UserData.set(message, 'count_photos', message.text)
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): '
                           f'Кол-во фото: {message.text}.')
            return True
        else:
            bot.send_message(message.from_user.id, 'Что-то пошло не так...\nНеверный ввод! Попробуй еще раз!')
            my_logger.info(f'{message.from_user.full_name} (id: {message.from_user.id}): Неверный ввод')
            return False


class FindHotels:

    @staticmethod
    def _create_querystring(pageNumber: str, request_data: dict) -> dict:
        querystring = {'destinationId': request_data['city']['destination_id'], 'pageNumber': pageNumber,
                       'pageSize': '25', 'checkIn': request_data['check_in'], 'checkOut': request_data['check_out'],
                       'adults1': '2', 'sortOrder': request_data['sort_order'], 'locale': LOCALE, 'currency': CURRENCY}
        if 'price_range' in request_data.keys():
            querystring.update({
                'priceMin': request_data['price_range'][0],
                'priceMax': request_data['price_range'][1]
            })
        return querystring

    @staticmethod
    def _parser_page(request_data: dict, page='1') -> list:
        url = START_URL + '/properties/list'
        count_days = DateWorker.count_days(request_data['check_in'], request_data['check_out'])

        querystring = FindHotels._create_querystring(pageNumber=str(page), request_data=request_data)
        data = APIHotels.request_api(url=url, headers=HEADERS, querystring=querystring)
        pattern = r'(?<=,)"results":.+?(?=,"pagination)'
        find = re.search(pattern, data)
        if find:
            hotels = list()
            data_json = json.loads(f"{{{find[0]}}}")
            for hotel in data_json['results']:
                rate = hotel['ratePlan']['price']['current']
                rate_all = float(rate[1:].replace(',', '.'))
                rate_all = int(rate_all) * count_days
                rate_all = rate[0] + str(rate_all)

                hotel_coordinate = (hotel['coordinate']['lat'], hotel['coordinate']['lon'])

                hotels.append({'id': hotel['id'],
                               'name': hotel['name'],
                               'address': hotel['address']['streetAddress'],
                               'rate': rate,
                               'rate_all': rate_all,
                               'coordinate': hotel_coordinate,
                               'url': 'https://www.hotels.com/ho' + str(hotel['id']),
                               })
            if not hotels:
                raise ValueError('Я не нашел отели по твоему запросу. Команда сброшена.')
            return hotels
        else:
            raise HTTPError('Не могу обработать ответ от сервера...\nКоманда сброшена. Выполни запрос позже.')

    @staticmethod
    def _parser_urls_photos(hotel_id: str, count_photos: str) -> list:
        url = START_URL + '/properties/get-hotel-photos'
        querystring = {"id": hotel_id}
        data = APIHotels.request_api(url=url, headers=HEADERS, querystring=querystring)
        pattern = r'(?<=,)"hotelImages":.+?(?=,"roomImages)'
        find = re.search(pattern, data)
        if find:
            data_json = json.loads(f"{{{find[0]}}}")
            urls_photos = list()
            for url_photo in data_json['hotelImages']:
                url_photo = url_photo['baseUrl'][0:-11] + '.jpg'
                urls_photos.append(url_photo)
                if len(urls_photos) == int(count_photos):
                    return urls_photos
            return urls_photos

    @staticmethod
    def _find_hotels(request_data: dict) -> list:
        count_hotels = int(request_data['count_hotels'])
        city_coordinate = request_data['city']['coordinate']
        hotels = list()
        for page in range(1, 5):
            page_hotels = FindHotels._parser_page(request_data=request_data, page=str(page))
            if request_data['command'] == '/bestdeal':
                min_dist, max_dist = request_data['distance_range']
                min_dist, max_dist = float(min_dist), float(max_dist)
                for hotel in page_hotels:
                    dist = distance(city_coordinate, hotel['hotel_coordinate']).km
                    if min_dist < dist < max_dist:
                        hotels.append(hotel)
                    if len(hotels) == count_hotels:
                        return hotels
            else:
                hotels = page_hotels[0:count_hotels]
                return hotels
        return hotels

    @staticmethod
    def result(message: Message, sort_order='PRICE') -> None:
        bot.send_message(message.from_user.id, 'Ищу отели...\nПодожди немного')
        UserData.set(message, 'sort_order', sort_order)

        data = UserData.get_all_value(message)
        try:
            hotels = FindHotels._find_hotels(request_data=data)
        except (HTTPError, ConnectionError, ValueError) as exc:
            bot.send_message(message.from_user.id, str(exc))
            UserData.reset(message)
            bot.delete_state(message.from_user.id, message.chat.id)
            my_logger.error(f'{message.from_user.full_name} (id: {message.from_user.id}): Ошибка на сервере.')
        else:
            for hotel in hotels:
                msg_text = f'Название отеля: {hotel["name"]}\n' \
                           f'Адрес: {hotel["address"]}\n' \
                           f'Стоимость одних суток: {hotel["rate"]}\n' \
                           f'Стоимость за весь период проживания: {hotel["rate_all"]}\n'

                markup = InlineMarkup.create_url_buttons([(hotel['name'], hotel['url'])])
                bot.send_message(message.from_user.id, msg_text, disable_web_page_preview=True, reply_markup=markup)

                if data['need_photos'].lower() == 'да':
                    urls_photos = FindHotels._parser_urls_photos(hotel['id'], data['count_photos'])
                    medias = [InputMediaPhoto(url_photo) for url_photo in urls_photos]
                    bot.send_media_group(message.from_user.id, medias)

            DataBaseWorker.add_row(
                user_id=message.from_user.id,
                name_cmd=data['command'],
                hotels=';'.join([hotel['name'] for hotel in hotels])
            )
            UserData.reset(message)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.from_user.id, 'Поиск закончен!', reply_markup=ReplyKeyboardRemove())





