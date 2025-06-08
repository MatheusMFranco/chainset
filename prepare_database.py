import os
import mysql.connector

HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
USER = os.getenv('MYSQL_USER', 'root')
PASSWORD = os.getenv('MYSQL_PASSWORD', 'admin')
DATABASE = os.getenv('MYSQL_DATABASE', 'chainset')

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return connection
    except mysql.connector.Error as error:
        return error

if __name__ == '__main__':
    connection = get_db_connection()
    if connection:
        print("Connected to the database successfully!")
        connection.close()
    else:
        print("Failed to connect to the database.")
