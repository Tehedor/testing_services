from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import mysql.connector
import os
from decimal import Decimal
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
CORS(app)
# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir todas las solicitudes de origen

# MongoDB connection
try:
    mongo_client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://mongodb-service:27017/'))
    mongo_db = mongo_client['financedb']
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# MySQL connection for financial data
try:
    mysql_conn_finances = mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'mysql_finances'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', 'password'),
        database=os.environ.get('MYSQL_DATABASE', 'financedb')
    )
    print("Connected to MySQL (finances)")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL (finances): {err}")

# MySQL connection for user authentication
try:
    mysql_conn_users = mysql.connector.connect(
        host=os.environ.get('MYSQL_USERDB_HOST', 'mysql_users'),
        user=os.environ.get('MYSQL_USERDB_USER', 'root'),
        password=os.environ.get('MYSQL_USERDB_PASSWORD', 'password'),
        database=os.environ.get('MYSQL_USERDB_DATABASE', 'userdb')
    )
    print("Connected to MySQL (users)")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL (users): {err}")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    print(f"Login attempt: username={username}, password={password}")
    
    cursor = mysql_conn_users.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        print(f"User found: {user}")
    else:
        print("User not found")
    
    if user and check_password_hash(user['password'], password):
        return jsonify({"status": "success", "message": "Login successful"}), 200
    else:
        return jsonify({"status": "failure", "message": "Invalid username or password"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    hashed_password = generate_password_hash(password)
    print(f"Register attempt: username={username}, email={email}")
    try:
        cursor = mysql_conn_users.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username, hashed_password, email)
        )
        mysql_conn_users.commit()
        cursor.close()
        return jsonify({"status": "success", "message": "User registered successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"status": "failure", "message": str(err)}), 400


@app.route('/data/mongodb', methods=['GET'])
def get_mongo_data():
    print("Getting data from MongoDB")
    try:
        data = list(mongo_db.finances.find({}, {'_id': 0}))
        print(f"MongoDB data: {data}")
        return jsonify(data)
    except Exception as e:
        print(f"Error getting data from MongoDB: {e}")
        return jsonify({"status": "failure", "message": str(e)}), 500

@app.route('/data/mongodb', methods=['POST'])
def add_mongo_data():
    data = request.json
    date = data.get('date')
    expense = data.get('expense')
    revenue = data.get('revenue')
    
    print(f"Adding data to MongoDB: date={date}, expense={expense}, revenue={revenue}")
    try:
        mongo_db.finances.insert_one({'date': date, 'expense': float(expense), 'revenue': float(revenue)})
        return jsonify({"status": "success", "message": "Data added to MongoDB"}), 201
    except Exception as e:
        print(f"Error adding data to MongoDB: {e}")
        return jsonify({"status": "failure", "message": str(e)}), 500

@app.route('/data/mysql', methods=['GET'])
def get_mysql_data():
    print("Getting data from MySQL")
    try:
        cursor = mysql_conn_finances.cursor(dictionary=True)
        cursor.execute("SELECT * FROM finances")
        data = cursor.fetchall()
        cursor.close()
        
        # Convertir los valores Decimal a números y formatear las fechas
        formatted_data = []
        for row in data:
            formatted_row = {
                'date': row['date'].strftime('%Y-%m-%d'),
                'expense': float(row['expense']),
                'revenue': float(row['revenue'])
            }
            formatted_data.append(formatted_row)
        
        print(f"MySQL data: {formatted_data}")
        return jsonify(formatted_data)
    except mysql.connector.Error as err:
        print(f"Error getting data from MySQL: {err}")
        return jsonify({"status": "failure", "message": str(err)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"status": "failure", "message": str(e)}), 500

@app.route('/data/mysql', methods=['POST'])
def add_mysql_data():
    data = request.json
    date = data.get('date')
    expense = data.get('expense')
    revenue = data.get('revenue')
    
    print(f"Adding data to MySQL: date={date}, expense={expense}, revenue={revenue}")
    try:
        cursor = mysql_conn_finances.cursor()
        cursor.execute(
            "INSERT INTO finances (date, expense, revenue) VALUES (%s, %s, %s)",
            (date, float(expense), float(revenue))
        )
        mysql_conn_finances.commit()
        cursor.close()
        return jsonify({"status": "success", "message": "Data added to MySQL"}), 201
    except mysql.connector.Error as err:
        print(f"Error adding data to MySQL: {err}")
        return jsonify({"status": "failure", "message": str(err)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)