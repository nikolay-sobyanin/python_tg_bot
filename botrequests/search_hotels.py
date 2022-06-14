import requests
from config import HOTELS_API_KEY


class SearchHotels:
    HOTELS_API_HOST = 'hotels4.p.rapidapi.com'
    URL = "https://hotels4.p.rapidapi.com"

    HEADERS = {
        "X-RapidAPI-Host": HOTELS_API_HOST,
        "X-RapidAPI-Key": HOTELS_API_KEY
    }

    def __init__(self):
        self.locale = 'en_US'
        self.currency = 'USD'

    def search_city(self, location: str):
        """
        :param location: Страна, регион, город
        :return: словарь с destination_id и наименование города, либо текст ошибки
        """
        connect, data = self._request_locations(location)
        if connect:
            result = self._handler_locations(data)
            return result
        else:
            return {'city_found': False, 'text_error': data}

    def _request_locations(self, location: str):
        """
        :param location: Страна, регион, город
        :return: словарь с данными о локациях, либо ошибка
        """
        url = self.URL + '/locations/v2/search'
        querystring = {'query': location, 'locale': self.locale, 'currency': self.currency}
        response = requests.request("GET", url, headers=self.HEADERS, params=querystring)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, 'Нет сооединения с сервером...\nПовторите запрос!'

    def _handler_locations(self, data: dict):
        """
        :param data: json с данными о локациях
        :return: данные о городе, либо ошибка
        """
        places = data['suggestions'][0]['entities']
        for place in places:
            if place['type'] == 'CITY':
                return {'city_found': True, 'destinationID': place['destinationId'], 'city_name': place['name']}
        else:
            return {'city_found': False, 'text_error': ' Я не нашел город...\nУточни запрос!'}

    def search_hotels(self, destination_id: str, count_hotels: int, check_in: str, check_out: str,
                      adults=2, sort_order='PRICE'):
        """
        :param destination_id: ID города
        :param count_hotels: сколько вывести отелей
        :param check_in: дата в формате yyyy-MM-dd
        :param check_out: дата в формате yyyy-MM-dd
        :param adults: количество людей для проживания
        :param sort_order: сортировать результат поиска. Значения: (BEST_SELLER, STAR_RATING_HIGHEST_FIRST,
        STAR_RATING_LOWEST_FIRST, DISTANCE_FROM_LANDMARK, GUEST_RATING, PRICE_HIGHEST_FIRST, PRICE)
        :return: список отелей
        """
        connect, data = self._request_hotels(destination_id, count_hotels, check_in, check_out, adults, sort_order)
        if connect:
            result = self._handler_hotels(data)
            return result
        else:
            return {'hotels_found': False, 'text_error': data}

    def _request_hotels(self, destination_id, count_hotels, check_in, check_out, adults, sort_order):
        url = self.URL + '/properties/list'
        querystring = {'destinationId': destination_id, 'pageNumber': '1', 'pageSize': str(count_hotels),
                       'checkIn': check_in, 'checkOut': check_out, 'adults1': str(adults), 'sortOrder': sort_order,
                       'locale': self.locale, 'currency': self.currency}
        response = requests.request("GET", url, headers=self.HEADERS, params=querystring)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, 'Нет сооединения с сервером...\nПовторите запрос!'

    def _handler_hotels(self, data):
        """
        :param data: json с данными о локациях
        :return: список отелей, либо ошибка
        """
        if data['result'] != 'OK':
            return {'hotels_found': False, 'text_error': ' Я не нашел отели по твоему запросу...\nПопробуй еще раз!'}

        found_hotels = data['data']['body']['searchResults']['results']
        if not found_hotels:
            return {'hotels_found': False, 'text_error': ' Я не нашел отели по твоему запросу...\nПопробуй еще раз!'}

        hotels = []
        for hotel in found_hotels:
            hotel_id = str(hotel['id'])
            name = hotel['name']
            address = hotel['address']['streetAddress']
            rate = hotel['ratePlan']['price']['current']
            hotels.append({'id': hotel_id, 'name': name, 'address': address, 'rate': rate})
        return {'hotels_found': True, 'hotels': hotels}

    def get_url_photos(self, hotels_id: list, count_photos: int):
        """
        :param hotels_id: ID отелей
        :param count_photos: количество фото отеля
        :return: словарь key: hotel_id, value: list of url photos
        """
        url_photos_hotels = {}
        for hotel_id in hotels_id:
            connect, data = self._request_url_photos(hotel_id)
            if connect:
                result = self._handler_url_photos(data, count_photos)
                url_photos_hotels[hotel_id] = {'photos_found': True, 'url': result}
            else:
                url_photos_hotels[hotel_id] = {'photos_found': False, 'text_error': data}

    def _request_url_photos(self, hotel_id):
        url = self.URL + '/properties/get-hotel-photos'
        querystring = {"id": hotel_id}
        response = requests.request("GET", url, headers=self.HEADERS, params=querystring)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, 'Нет сооединения с сервером...\nПовторите запрос!'

    def _handler_url_photos(self, data, count_photos):
        url_photos = []
        for photo in data['hotelImages']:
            url_photo = photo['baseUrl'][0:-11] + '.jpg'
            url_photos.append(url_photo)
            if len(url_photos) == count_photos:
                return url_photos
        else:
            return url_photos

