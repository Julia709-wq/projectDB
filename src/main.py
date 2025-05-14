import psycopg2

from dotenv import load_dotenv
from hh_api import HeadHunterAPI
from src.db_manager import DBManager
from src.db_utils import fill_employers_tables, fill_vacancies_table


def main():
    """Функция взаимодействия с пользователем"""

    hh_api = HeadHunterAPI()
    vacancies_data = hh_api.get_data()  # список словарей

    load_dotenv('.env') # не работает
    user = 'postgres'
    password = '0'
    new_db = str(input("Введите название базы данных, с которой хотите работать: "))

    db_conn = DBManager(new_db, user=user,
                        password=password)
    db_cur = db_conn.cur

    create_tab1_command = """CREATE TABLE IF NOT EXISTS employers (
                 id VARCHAR PRIMARY KEY,
                 company_name VARCHAR
                 )"""
    create_tab2_command = """CREATE TABLE IF NOT EXISTS vacancies (
                 id VARCHAR PRIMARY KEY,
                 name VARCHAR,
                 salary INT,
                 url VARCHAR,
                 employer_id VARCHAR,
                 FOREIGN KEY (employer_id) REFERENCES employers(id))"""

    try:
        db_cur.execute(create_tab1_command)
        db_cur.execute(create_tab2_command)
        print("Таблицы успешно созданы.")

    except (Exception, psycopg2.OperationalError) as e:
        print("Ошибка при создании таблиц: ", e)

    fill_employers_tables(vacancies_data, db_cur)
    fill_vacancies_table(vacancies_data, db_cur)


main()
