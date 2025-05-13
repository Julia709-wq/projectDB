import requests
from src.api_base import BaseAPI


class HeadHunterAPI(BaseAPI):
    """Класс для работы с hh.ru"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-API-Client"}

    def _connect_(self, params: dict) -> list:
        """Приватный метод для подключения к API"""
        response = requests.get(
            url=self.__url,
            headers=self.__headers,
            params=params
        )

        if response.status_code != 200:
            print(f"Ошибка при подключении к API: {response.reason}")

        return response.json()

    def get_data(self, keyword: str) -> list:
        """Метод получения данных по поисковому запросу"""
        params = {"text": keyword,
                  "per_page": 30}

        data = self._connect_(params)
        return data['items']


hh1 = HeadHunterAPI()
print(hh1.get_data('оператор'))
