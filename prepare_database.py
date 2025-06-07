import os
import mysql.connector

HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
USER = os.getenv('MYSQL_USER', 'root')
PASSWORD = os.getenv('MYSQL_PASSWORD', 'admin')
DATABASE = os.getenv('MYSQL_DATABASE', 'jogoteca')

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return conn
    except mysql.connector.Error as err:
        return None

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        print("Connected to the database successfully!")
        conn.close()
    else:
        print("Failed to connect to the database.")
