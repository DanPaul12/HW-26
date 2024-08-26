from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Int(dump_only = True)
    name = fields.String(required = True)
    age = fields.String(required = True)

    class Meta:
        fields = ("id", "name", "age")

class WorkoutSchema(ma.Schema):
    session_id = fields.String(dump_only = True)
    member_id = fields.String(required = True)
    date = fields.String(required = True)
    time = fields.String(required = True)
    activity = fields.String(required = True)
    
    class Meta:
        fields = ("session_id", "member_id", "date", "time", "activity")

member_schema = MemberSchema()
members_schema = MemberSchema(many = True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many = True)

#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

@app.route('/')
def home():
    return"Welcome"

#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

@app.route('/members/<int:id>', methods = ["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary = True, buffered = True)
        query = "UPDATE Members SET name = %s, age = %s where id = %s"
        
        cursor.execute(query, (member_data['name'], member_data['age'], id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "member updated"}), 201
    except Error as e:
        print({e})
        return jsonify({"error": 'internal server error'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    

#-----------------------------------------------------------------------

@app.route('/members/<int:id>', methods = ["DELETE"])
def delete_member(id):
    conn = get_db_connection()
    if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        query = "DELETE from Members where id = %s"
        cursor.execute(query,(id,))
        conn.commit()
        return jsonify({"message":"member deleted"}), 200
    except Error as e:
        return jsonify({e})
    finally:
        cursor.close()
        conn.close()

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

@app.route('/workouts', methods = ["GET"])
def get_workouts():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor(dictionary = True, buffered = True)

        query = "SELECT * from WorkoutSessions"

        cursor.execute(query)

        workouts = cursor.fetchall()

        return workouts_schema.jsonify(workouts)
    except Error as e:
        print({e})
        return jsonify({"error": 'internal server error'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#-----------------------------------------------------------------------

@app.route('/workouts/<int:session_id>', methods = ["GET"])
def get_workout(session_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error":"Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary = True)
        cursor.execute("SELECT * from WorkoutSessions where id = %s", (session_id,))
        workout = cursor.fetchone()
        cursor.close()
        conn.close()
        if workout:
            return workout_schema.jsonify(workout)
        else:
            return jsonify({'error':"workout not found"}), 404
    except Error as e:
        return ({e})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(debug= True)



    