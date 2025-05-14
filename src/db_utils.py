import psycopg2

def fill_employers_tables(data: list, cur):
    """Функция заполнения таблицы с данными о работодателях"""
    top_employers = ['Wildberries', 'VK', 'Great', 'ВкусВилл', 'Яндекс',
                     'Altenar', 'ВТБ АРЕНА', 'Лаборатория Гемотест',
                     'Пятёрочка', 'АЛРОСА']
    unique_employers = {}

    for i in data:
        emp_name = i.get('employer', {}).get('name')
        emp_id = i.get('employer', {}).get('id')

        if emp_name in top_employers and emp_id not in unique_employers:
            unique_employers[emp_id] = emp_name

    try:
        for emp_id, emp_name in unique_employers.items():
            cur.execute("""
                INSERT INTO employers VALUES
                (%s, %s)
                ON CONFLICT(id) DO NOTHING;
                """, (emp_id, emp_name)
            )
        print("Данные о работодателях добавлены в таблицу.")
        cur.execute("SELECT * FROM employers;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except (psycopg2.IntegrityError, psycopg2.ProgrammingError) as e:
        print("Ошибка добавления данных в таблицу: ", e)
        cur.connection.rollback()

def fill_vacancies_table(data: list, cur):
    """Функция заполнения таблицы с данными о вакансиях"""
    top_employers = ['Wildberries', 'VK', 'Great', 'ВкусВилл', 'Яндекс',
                     'Altenar', 'ВТБ АРЕНА', 'Лаборатория Гемотест',
                     'Пятёрочка', 'АЛРОСА']

    for vac in data:
        emp_name = vac.get('employer', {}).get('name')
        emp_id = vac.get('employer', {}).get('id')

        if emp_name not in top_employers:
            continue

        vac_id = vac.get("id")
        name = vac.get("name")
        url = vac.get("url")

        salary_data = vac.get("salary")
        salary = None
        if salary_data:
            salary = salary_data.get("from") or salary_data.get("to")

        try:
            cur.execute(
                """
                INSERT INTO vacancies (id, name, salary, url, employer_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (vac_id, name, salary, url, emp_id)
            )
            print("Вакансии успешно добавлены в таблицу.")
            cur.execute("SELECT * FROM vacancies;")
            rows = cur.fetchall()
            for row in rows:
                print(row)

        except psycopg2.IntegrityError as e:
            print(f"Ошибка целостности данных при вставке вакансии {vac_id}: ", e)
            cur.connection.rollback()
        except Exception as e:
            print(f"Ошибка при вставке вакансии {vac_id}: ", e)
