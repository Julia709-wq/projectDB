import psycopg2

from db_utils import ensure_database_exists
from hh_api import HeadHunterAPI
from src.db_utils import fill_tables

# получение данных от API по ключевому слову
hh_api = HeadHunterAPI()
keyword = input("Введите поисковый запрос: ")
raw_vac = hh_api.get_data(keyword)  # список словарей

# создание новой БД для дальнейшей работы
new_db = str(input("Введите название базы данных, с которой хотите работать: "))
conn = ensure_database_exists('postgres', '0', 'localhost', new_db)
cur = conn.cursor()

# создание таблиц
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
    cur.execute(create_tab1_command)
    cur.execute(create_tab2_command)
    print("Таблицы успешно созданы.")
except (Exception, psycopg2.OperationalError) as e:
    print("Ошибка при создании таблиц: ", e)

data = fill_tables(raw_vac)
try:
    for employer in data:
        cur.execute("""
            INSERT INTO employers VALUES
            (%s, %s)
            ON CONFLICT(id) DO NOTHING;
            """, (employer["emp_id"], employer["emp_name"])
        )
    print("Данные о работодателях добавлены в таблицу.")
    cur.execute("SELECT * FROM employers;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
except (psycopg2.IntegrityError, psycopg2.ProgrammingError) as e:
    print("Ошибка добавления данных в таблицу: ", e)
