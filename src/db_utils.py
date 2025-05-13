import psycopg2
import sql

def ensure_database_exists(username, password, host, db_name):
    # сначала подключаемся к системной базе postgres
    conn = psycopg2.connect(
        database="postgres",
        user=username,
        password=password,
        host=host
    )
    conn.autocommit = True
    cur = conn.cursor()

    # проверяем, существует ли нужная база
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
    exists = cur.fetchone()

    if exists:
        print(f"База данных '{db_name}' уже существует. Подключение...")
    else:
        print(f"База данных '{db_name}' не существует. Создаём...")
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"База данных '{db_name}' успешно создана.")

    cur.close()
    conn.close()

    # возвращаем соединение к нужной БД
    return psycopg2.connect(
        database=db_name,
        user=username,
        password=password,
        host=host
    )


def fill_tables(data):
    top_employers = ['Ермак-УФА', 'Мистер Крабс', 'ВкусВилл', 'МагКомпозит', 'Ozon']
    unique_employers = {}
    for i in data:
        emp_name = i['employer']['name']
        emp_id = i['employer']['id']

        if emp_name in top_employers and emp_id not in unique_employers:
            unique_employers[emp_id] = emp_name

    return [{"emp_id": eid, "emp_name": name} for eid, name in unique_employers.items()]
