import mysql.connector # importing the mysql connector that we just pip installed
from mysql.connector import Error # Importing the mysql Error package to deal with specific errors

db_name = 'ecom'
user = 'root'
password = 'Blessedone1!'
host = 'localhost'

def connection():
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        if conn.is_connected():
            print('Sucessfully Connected to MySQL database')
            return conn

    except Error as e:
            print(f'Error connecting to MySQL: {e}')
            return None

