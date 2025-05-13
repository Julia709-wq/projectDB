from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_(self, params: dict):
        """Абстрактный метод подключения к API"""
        pass

    @abstractmethod
    def get_data(self, keyword: str):
        """Абстрактный метод получения данных от API"""
        pass
