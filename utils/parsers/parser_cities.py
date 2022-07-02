import re
import json
from config_data.config import START_URL, HEADERS, LOCALE, CURRENCY
from utils.request_to_api_hotels import request_to_api


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
            cities.append({'city_name': city_name, 'destination_id': city['destinationId']})
        return cities
