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
	json_data_with_indent = json.dumps(data, indent=4)
	print(f'Та же строка, но уже с отступами, в удобном виде: {json_data_with_indent}')
	with open('search_locations_success.json', 'w') as file:
		file.write(json_data_with_indent)


city = 'Франция, Париж'

search_locations(location=city)
