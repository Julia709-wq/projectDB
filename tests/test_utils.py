from src.db_utils import fill_vacancies_table,fill_employers_tables


def test_fill_employers_table(mock_cursor):
    data = [{"employer": {"id": "1", "name": "Wildberries"}},
            {"employer": {"id": "2", "name": "VK"}},
            {"employer": {"id": "3", "name": "SomeCompany"}},
            {"employer": {"id": "1", "name": "Wildberries"}},
            ]

    fill_employers_tables(data, mock_cursor)

    assert mock_cursor.execute.call_count >= 3
    mock_cursor.fetchall.assert_called_once()
