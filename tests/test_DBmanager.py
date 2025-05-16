def test_get_companies_and_vacancies_count(sample_db):
    comp_and_vacs = sample_db.get_companies_and_vacancies_count()
    assert len(comp_and_vacs) == 2
    assert comp_and_vacs[0][1] == 2


def test_get_all_vacancies(sample_db):
    vacancies = sample_db.get_all_vacancies()
    assert len(vacancies) == 3
    assert vacancies[0][1] == 'Python Developer'


def test_get_vacancies_with_higher_salary(sample_db):
    vacancies = sample_db.get_vacancies_with_higher_salary()
    assert len(vacancies) == 2


def test_get_vacancies_with_keyword(sample_db):
    keyword1 = "Developer"
    result1 = sample_db.get_vacancies_with_keyword(keyword1)
    assert len(result1) == 3

    keyword2 = "Python"
    result1 = sample_db.get_vacancies_with_keyword(keyword2)
    assert len(result1) == 1
