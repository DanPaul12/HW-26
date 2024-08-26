from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Int(dump_only = True)
    name = fields.String(required = True)
    age = fields.String(required = True)

    class Meta:
        fields = ("id", "name", "age")

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
            return conn
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
        cursor = conn.cursor(dictionary = True, buffered = True)

        query = "SELECT * from Members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    except Error as e:
        print({e})
        return jsonify({"error": 'internal server error'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods = ["GET"])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary = True, buffered = True)
        cursor.execute("SELECT * from Members where id = %s", (id,))
        member = cursor.fetchone()
        cursor.close()
        conn.close()

        if member:
            return member_schema.jsonify(member)
        else:
            return jsonify({'error':"member not found"}), 404
    except Error as e:
        print({e})
        return jsonify({"error": 'internal server error'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members', methods = ["POST"])
def add_member():
    try:
       member_data = member_schema.load(request.json)
    except ValidationError as e:
        print({e})
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        member = member_data["name"], member_data['age']
        
        cursor = conn.cursor(buffered = True)

        query = "INSERT INTO Members  (name, age) Values (%s, %s)"

        cursor.execute(query, member)
        conn.commit()
        return jsonify({'message': 'member added successfully'}), 201
    except Error as e:
        print({e})
        return jsonify({"error": 'internal server error'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    

if __name__ == "__main__":
    app.run(debug= True)



    