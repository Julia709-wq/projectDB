from unittest.mock import patch
from src.hh_api import HeadHunterAPI


@patch('requests.get')
def test_get_data(mock_get, sample_api_response):
    """Проверка получения данных от API"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = sample_api_response

    api = HeadHunterAPI()
    result = api.get_data()

    assert isinstance(result, list)
    assert len(result) == 2
