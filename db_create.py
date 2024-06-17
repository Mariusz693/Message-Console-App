from db_settings import DB_USER, DB_PASSWORD, DB_HOST
from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

DB_NAME = "message_console_app"

CREATE_USERS_TABLE = """
    CREATE TABLE users(
        id serial PRIMARY KEY,
        username varchar(255) UNIQUE,
        hashed_password varchar(80)
    );
"""

CREATE_MESSAGES_TABLE = """
    CREATE TABLE messages(
        id serial PRIMARY KEY,
        from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        text varchar(255),
        date_of_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""


def create_database():
    try:
        cnx = connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cnx.autocommit = True
        cursor = cnx.cursor()
        try:
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
            print('Database created')
        except DuplicateDatabase:
            print('Database exists')
    except OperationalError as e:
        print('Connection error: ', e)
    finally:
        cursor.close()
        cnx.close()


def create_table():
    try:
        cnx = connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME
        )
        cnx.autocommit = True
        cursor = cnx.cursor()
        try:
            cursor.execute(CREATE_USERS_TABLE)
            print('Table users created')
        except DuplicateTable:
            print('Table users exists')
        try:
            cursor.execute(CREATE_MESSAGES_TABLE)
            print('Table messages created')
        except DuplicateTable:
            print('Table messages exists')
    except OperationalError as e:
        print('Connection error: ', e)
    finally:
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    create_database()
    create_table()