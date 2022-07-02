import re
import json
from config_data.config import START_URL, HEADERS, LOCALE, CURRENCY
from utils.request_to_api_hotels import request_to_api


def find_urls_photos(hotel_id: str, count_photos: str) -> list:
    url = START_URL + '/properties/get-hotel-photos'
    querystring = {"id": hotel_id}
    data_text = request_to_api(url=url, headers=HEADERS, querystring=querystring)
    pattern = r'(?<=,)"hotelImages":.+?(?=,"roomImages)'
    find = re.search(pattern, data_text)
    if find:
        data_json = json.loads(f"{{{find[0]}}}")
        urls_photos = list()
        for url_photo in data_json['hotelImages']:
            url_photo = url_photo['baseUrl'][0:-11] + '.jpg'
            urls_photos.append(url_photo)
            if len(urls_photos) == int(count_photos):
                return urls_photos
        return urls_photos
