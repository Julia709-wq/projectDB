import pytest
from src.db_manager import DBManager


@pytest.fixture
def sample_api_response() -> dict:
    return {
        "items": [
            {"name": "Backend разработчик", "salary":
                {'from': 100000, 'to': 150000}},
            {"name": "Frontend разработчик", "salary":
                {'from': 80000, 'to': 100000}}
        ]
    }


@pytest.fixture
def sample_db():
    user = 'postgres'
    password = '0'
    db = DBManager("test_db", user, password)

    db.cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id VARCHAR PRIMARY KEY,
                company_name VARCHAR
            );
        """)
    db.cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id VARCHAR PRIMARY KEY,
                name VARCHAR,
                salary INT,
                url VARCHAR,
                employer_id VARCHAR REFERENCES employers(id)
            );
        """)

    db.delete_data()
    data1 = [("123", "Company1"), ("124", "Company2")]
    db.cur.executemany("INSERT INTO employers VALUES (%s, %s);",
                       data1)

    data2 = [("1", "Python Developer", 150000, "http://sample.com/vac1", "123"),
             ("2", "Java Developer", 130000, "https://sample.com/vac2", "123"),
             ("3", "Frontend Developer", 100000, "https://sample.com/vac3", "124")]
    db.cur.executemany("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s);", data2)

    db.conn.commit()
    return db
