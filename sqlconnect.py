import mysql.connector
from mysql.connector import Error

def get_db_connection():
    db_name = "fitness_center_db"
    user = "root"
    host = "localhost"
    password = "thegoblet2"
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            host = host,
            password = password
        )
        if conn is not None:
            print("Connection succcessful")
    except Error as e:
        print({e})
