from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required = True)
    age = fields.String(required = True)

    class Meta:
        fields = ("name", "age")

member_schema = MemberSchema()
members_schema = MemberSchema(many = True)


def get_db_connection():
    db_name = "fitness_center_db"
    user = "root"
    host = "localhost"
    password = "thegoblet2"
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )
        if conn is not None:
            print("Connection succcessful")
    except Error as e:
        print({e})



@app.route('/')
def home():
    return"Welcome"

@app.route('/members', methods = ["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor(dictionary = True)

        query = "SELECT * from Members"

        cursor.execute(query)

        members = cursor.fetchall

        return members_schema.jsonify(members)
    except Error as e:
        print({e})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app.run(debug= True)



    