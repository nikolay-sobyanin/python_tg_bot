import requests
from requests.exceptions import HTTPError, ConnectionError


def request_to_api(url, headers, querystring) -> str:
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        if response.status_code == requests.codes.ok:
            return response.text
        else:
            raise HTTPError
    except (HTTPError, ConnectionError):
        print('Ошибка соединения с сервером')

