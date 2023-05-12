import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


# SELECT SQL queries
def get_id_from_urls(url):
    """Return url_id or None"""
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute(
                "SELECT id FROM urls WHERE name = %s", (url,)
            )
            url_id = curs.fetchone()
    conn.close()
    return url_id


def get_urls_data():
    """
    Return urls.id, urls.name, url_checks.created_at, url_checks.status_code
    for all urls
    """
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT urls.id, urls.name, url_checks.created_at, url_checks.status_code "
                         "FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                         "WHERE url_checks.url_id IS NULL OR "
                         "url_checks.id = (SELECT MAX(url_checks.id) "
                         "FROM url_checks WHERE url_checks.url_id = urls.id) "
                         "ORDER BY urls.id DESC")
            url_data = curs.fetchall()
    conn.close()
    return url_data


def get_url_info(id):
    """Return id, name, created_at FROM urls"""
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name, created_at FROM urls WHERE id = %s", (id,))
            url_info = curs.fetchone()
    conn.close()
    return url_info


def get_check_info(id):
    """Return check results"""
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM url_checks WHERE url_id = %s", (id,))
            check_result = curs.fetchall()
    conn.close()
    return check_result


# INSERT SQL queries
def add_url_into_db(url, today):
    """Add record into table urls"""
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("INSERT INTO urls (name, created_at) "
                         "VALUES (%s, %s) RETURNING id",
                         (url, today))
            result = curs.fetchone()
    conn.close()
    return result


def insert_check_result(id, data, today_date):
    """Add check result into db"""
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("INSERT INTO url_checks "
                         "(url_id, status_code, h1, title, description, created_at) "
                         "VALUES (%s, %s, %s, %s, %s, %s)",
                         (id, data['status_code'], data['h1'],
                          data['title'], data['description'], today_date,))
    conn.close()
