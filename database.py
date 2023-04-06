import psycopg2
from config import host, user, password, db_name

conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

conn.autocommit = True


def create_table_viewed():
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS viewed(
                        id SERIAL,
                        profile_id INTEGER,
                        worksheet_id INTEGER UNIQUE)""")
    print('БД - Таблица viewed создана.')


def insert_data_viewed(profile_id, worksheet_id):
    with conn.cursor() as cur:
        cur.execute(
            f"""INSERT INTO viewed (profile_id, worksheet_id) 
            VALUES ('{profile_id}', '{worksheet_id}')""")
        conn.commit()


def select_of_unviewed(profile_id):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT worksheet_id FROM viewed WHERE profile_id=%s;""", (profile_id,))
        return cursor.fetchall()