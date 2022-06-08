import requests
import json

HOTELS_API_HOST = 'hotels4.p.rapidapi.com'
HOTELS_API_KEY = '325dd5c577msh657b82a1b3b1193p133c7ejsn9e9440f768b6'

URL_START = "https://hotels4.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Host": HOTELS_API_HOST,
    "X-RapidAPI-Key": HOTELS_API_KEY
}


def search_locations(location: str, locale='en_US', currency='USD'):
    url = URL_START + '/locations/v2/search'
    querystring = {'query': location, 'locale': locale, 'currency': currency}
    response = requests.request("GET", url, headers=HEADERS, params=querystring)
    data = response.json()

    with open('response_JSON/search_locations.json', 'w') as file:
        json.dump(data, file, indent=4)


#  The check-in/out date at hotel, formated as yyyy-MM-dd

#  sortOrder One of the following is allowed BEST_SELLER|STAR_RATING_HIGHEST_FIRST|STAR_RATING_LOWEST_FIRST|
#  DISTANCE_FROM_LANDMARK|GUEST_RATING|PRICE_HIGHEST_FIRST|PRICE
def search_hotels(destinationId: str, checkIn: str, checkOut: str, adults: str, sortOrder: str, locale='en_US', currency='USD'):
    url = URL_START + '/properties/list'

    querystring = {"destinationId": destinationId, "pageNumber": "1", "pageSize": "25", "checkIn": checkIn,
                   "checkOut": checkOut, "adults1": adults, "sortOrder": sortOrder, "locale": locale, "currency": currency}

    response = requests.request("GET", url, headers=HEADERS, params=querystring)
    data = response.json()

    with open('response_JSON/search_hotels_high.json', 'w') as file:
        json.dump(data, file, indent=4)


def get_details_hotel(hotel_id: str, checkIn: str, checkOut: str, adults: str, locale='en_US', currency='USD'):
    url = URL_START + '/properties/get-details'

    querystring = {"id": hotel_id, "checkIn": checkIn, "checkOut": checkOut, "adults1": adults , "currency": currency, "locale": locale}

    response = requests.request("GET", url, headers=HEADERS, params=querystring)
    data = response.json()

    with open('response_JSON/details_hotel.json', 'w') as file:
        json.dump(data, file, indent=4)


def get_photos_hotel(hotel_id: str):
    url = URL_START + '/properties/get-hotel-photos'

    querystring = {"id": hotel_id}

    response = requests.request("GET", url, headers=HEADERS, params=querystring)
    data = response.json()

    with open('response_JSON/photos_hotel.json', 'w') as file:
        json.dump(data, file, indent=4)


get_photos_hotel(hotel_id='468076')
