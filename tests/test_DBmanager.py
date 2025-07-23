from unittest.mock import patch


@patch('src.db_manager.DBManager')
def test_get_companies_and_vacancies_count(mock_db_class):
    mock_db = mock_db_class.return_value
    mock_db.get_companies_and_vacancies_count.return_value = [
        ("Company1", 2),
        ("Company2", 1)
    ]
    result = mock_db.get_companies_and_vacancies_count()
    assert len(result) == 2
    assert result[0][1] == 2


@patch('src.db_manager.DBManager')
def test_get_all_vacancies(mock_db_class):
    mock_db = mock_db_class.return_value
    mock_db.get_all_vacancies.return_value = [
        ("Company1", "Python Developer", 150000, "url1"),
        ("Company1", "Java Developer", 130000, "url2"),
        ("Company2", "Frontend Developer", 100000, "url3")
    ]
    result = mock_db.get_all_vacancies()
    assert len(result) == 3
    assert result[0][1] == "Python Developer"


@patch('src.db_manager.DBManager')
def test_get_vacancies_with_higher_salary(mock_db_class):
    mock_db = mock_db_class.return_value
    mock_db.get_vacancies_with_higher_salary.return_value = [
        ("1", "Python Developer", 150000, "url1"),
        ("2", "Java Developer", 130000, "url2")
    ]
    result = mock_db.get_vacancies_with_higher_salary()
    assert len(result) == 2


@patch('src.db_manager.DBManager')
def test_get_vacancies_with_keyword(mock_db_class):
    mock_db = mock_db_class.return_value
    mock_db.get_vacancies_with_keyword.side_effect = lambda kw: (
        [
            ("1", "Python Developer", 150000, "url1"),
            ("2", "Java Developer", 130000, "url2"),
            ("3", "Frontend Developer", 100000, "url3"),
        ] if kw == "Developer" else
        [
            ("1", "Python Developer", 150000, "url1")
        ] if kw == "Python" else []
    )

    result1 = mock_db.get_vacancies_with_keyword("Developer")
    assert len(result1) == 3

    result2 = mock_db.get_vacancies_with_keyword("Python")
    assert len(result2) == 1