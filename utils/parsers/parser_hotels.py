import re
import json
from config_data.config import START_URL, HEADERS, LOCALE, CURRENCY
from .request_to_api_hotels import request_to_api
from utils import date_worker


def find_hotels(**kwargs) -> list:
    url = START_URL + '/properties/list'
    querystring = {'destinationId': kwargs['destination_id'], 'pageNumber': '1', 'pageSize': kwargs['count_hotels'],
                   'checkIn': kwargs['check_in'], 'checkOut': kwargs['check_out'], 'adults1': '2',
                   'sortOrder': kwargs['sort_order'], 'locale': LOCALE, 'currency': CURRENCY}

    data_text = request_to_api(url=url, headers=HEADERS, querystring=querystring)
    pattern = r'(?<=,)"results":.+?(?=,"pagination)'
    find = re.search(pattern, data_text)
    if find:
        count_days = date_worker.get_count_days(kwargs['check_in'], kwargs['check_out'])
        data_json = json.loads(f"{{{find[0]}}}")
        hotels = list()
        for hotel in data_json['results']:
            rate = hotel['ratePlan']['price']['current']
            hotels.append({'id': str(hotel['id']),
                           'name': hotel['name'],
                           'address': hotel['address']['streetAddress'],
                           'rate': rate,
                           'rate_all': rate[0] + str(float(rate[1:]) * count_days),
                           'url': 'https://www.hotels.com/ho' + str(hotel['id']),
                           })
        return hotels
