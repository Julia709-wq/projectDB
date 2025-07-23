from src.db_utils import fill_employers_tables
from unittest.mock import patch, MagicMock


@patch('src.db_utils.psycopg2')
def test_fill_employers_table(_):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [('1', 'Wildberries'), ('2', 'VK')]

    data = [{"employer": {"id": "1", "name": "Wildberries"}},
            {"employer": {"id": "2", "name": "VK"}},
            {"employer": {"id": "3", "name": "SomeCompany"}},
            {"employer": {"id": "1", "name": "Wildberries"}},
            ]

    fill_employers_tables(data, mock_cursor)

    assert mock_cursor.execute.call_count >= 3
    mock_cursor.fetchall.assert_called_once()
