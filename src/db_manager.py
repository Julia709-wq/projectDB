import psycopg2
from psycopg2 import sql


class DBManager:
    """Класс для работы с запросами к базе данных"""

    def __init__(self, db_name: str, user: str, password: str,
                 host: str = "localhost"):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.conn = self._connect_to_db()
        self.cur = self.conn.cursor()
        print("Подключение к базе данных установлено.")

    def _connect_to_db(self):
        """Подключение к базе данных"""

        # сначала подключаемся к системной базе postgres
        sys_conn = psycopg2.connect(
            database="postgres",
            user=self.user,
            password=self.password,
            host=self.host
        )
        sys_conn.autocommit = True
        sys_cur = sys_conn.cursor()

        # проверяем, существует ли нужная база
        sys_cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;",
                        (self.db_name,))
        exists = sys_cur.fetchone()

        if exists:
            print(f"База данных '{self.db_name}' уже существует. "
                  f"Подключение...")
        else:
            print(f"База данных '{self.db_name}' не существует. Создаём...")
            sys_cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.db_name)))
            print(f"База данных '{self.db_name}' успешно создана.")

        sys_cur.close()
        sys_conn.close()

        # возвращаем соединение к нужной БД
        return psycopg2.connect(
            database=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host
        )

    def get_companies_and_vacancies_count(self):
        """Подсчет вакансий каждой компании"""
        self.cur.execute("""
            SELECT  e.company_name, COUNT(v.id)
            FROM employers e JOIN vacancies v
            ON e.id = v.employer_id
            GROUP BY e.id;
            """)

        rows = self.cur.fetchall()
        print("\nНазвание компании || Количество вакансий\n")
        for row in rows:
            print(row)

        return rows

    def get_all_vacancies(self):
        """Получение списка всех вакансий"""
        self.cur.execute("""
            SELECT e.company_name, v.name,
            v.salary, v.url
            FROM employers e JOIN vacancies v
            ON e.id = v.employer_id;
            """)

        rows = self.cur.fetchall()
        print("\nСписок вакансий:\n")
        for row in rows:
            print(row)

        return rows

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям"""
        self.cur.execute("""
            SELECT AVG(salary)
            FROM vacancies;
            """)

        rows = self.cur.fetchall()
        print("\nСредняя зарплата по вакансиям:\n")
        for row in rows:
            print(row)

        return rows

    def get_vacancies_with_higher_salary(self):
        """Получение списка вакансий с зарплатами выше средней"""
        self.cur.execute("""
            SELECT id, name, salary, url
            FROM vacancies
            WHERE salary > (SELECT AVG(salary) FROM vacancies);
            """)

        rows = self.cur.fetchall()
        print("\nВакансии с зарплатой выше средней:\n")
        for row in rows:
            print(row)

        return rows

    def get_vacancies_with_keyword(self, keyword: str):
        """Получение списка всех вакансий с ключевым словом"""
        self.cur.execute("""
            SELECT id, name, salary, url
            FROM vacancies
            WHERE name LIKE %s
            """, (f"%{keyword}%",))

        rows = self.cur.fetchall()
        print(f"\nВакансии с ключевым словом {keyword}:\n")
        for row in rows:
            print(row)

        return rows

    def delete_data(self):
        """Метод очистки таблиц (для удобства)"""
        self.cur.execute("DELETE FROM vacancies;")
        self.cur.execute("DELETE FROM employers;")
