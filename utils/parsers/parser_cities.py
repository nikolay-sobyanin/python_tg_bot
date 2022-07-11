import re
import json
from config_data.config import START_URL, HEADERS, LOCALE, CURRENCY
from .request_to_api_hotels import request_to_api
from requests.exceptions import HTTPError


def find_cities(city: str) -> list:
    url = START_URL + '/locations/v2/search'
    querystring = {'query': city, 'locale': LOCALE, 'currency': CURRENCY}
    data_text = request_to_api(url=url, headers=HEADERS, querystring=querystring)
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
