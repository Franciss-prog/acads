import pymysql
from pymysql.cursors import DictCursor


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="library",
        cursorclass=DictCursor,
    )


def test_connection():
    try:
        connection = get_db_connection()
        connection.close()
        print("Connected to the database")
    except Exception as e:
        print("Error connecting to the database:", e)
