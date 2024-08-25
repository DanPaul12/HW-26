from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
ma = Marshmallow(app)

def get_db_connection():
    db_name = "fitness_center_db"
    user = "root"
    host = "localhost"
    password = "thegoblet2"
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            hot = host,
            password = password
        )
        if conn is not None:
            print("Connection succcessful")
    except Error as e:
        print({e})

@app.route('/')
def home():
    return"Welcome"

if __name__ == "__main__":
    app.run(debug= True)


def get_member(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error":"Database connection failed"}), 500
    cursor = conn.cursor()

    