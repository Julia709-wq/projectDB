import os
from dotenv import load_dotenv

from hh_api import HeadHunterAPI
from src.db_manager import DBManager
from src.db_utils import fill_employers_tables, fill_vacancies_table, create_tables


def main():
    """Функция взаимодействия с пользователем"""

    hh_api = HeadHunterAPI()
    vacancies_data = hh_api.get_data()  # список словарей

    load_dotenv()
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    new_db = str(input("Введите название базы данных, с которой хотите работать: "))

    db_conn = DBManager(new_db, user=user,
                        password=password)
    db_cur = db_conn.cur

    create_tables(db_cur)

    fill_employers_tables(vacancies_data, db_cur)
    fill_vacancies_table(vacancies_data, db_cur)

    while True:
        try:
            num = int(input("""Таблицы заполнены. Введите пункт меню:\n
1. Подсчитать вакансии каждой компании\n
2. Получить список всех вакансий\n
3. Получить среднюю зарплату по вакансиям\n
4. Получить список вакансий с зарплатами выше средней\n
5. Получить список вакансий с ключевым словом\n
6. Выход\n"""))

            if num == 1:
                db_conn.get_companies_and_vacancies_count()
            elif num == 2:
                db_conn.get_all_vacancies()
            elif num == 3:
                db_conn.get_avg_salary()
            elif num == 4:
                db_conn.get_vacancies_with_higher_salary()
            elif num == 5:
                kw = input("Введите ключевое слово: ")
                db_conn.get_vacancies_with_keyword(kw)
            elif num == 6:
                print("Выход из программы")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")

        except ValueError:
            print("Введите целое число.")

    db_conn.conn.commit()


main()
