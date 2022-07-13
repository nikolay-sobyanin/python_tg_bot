import requests
from requests.exceptions import HTTPError, ConnectionError


class APIHotels:

    @staticmethod
    def request_api(url, headers, querystring) -> str:
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            if response.status_code == requests.codes.ok:
                return response.text
            else:
                raise HTTPError
        except HTTPError:
            raise HTTPError('Не могу связаться с сервером...\nКоманда сброшена. Выполни запрос позже.')
        except ConnectionError:
            raise ConnectionError('Не могу связаться с сервером...\nКоманда сброшена. Выполни запрос позже.')
