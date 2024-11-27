from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import mysql.connector
import os
from decimal import Decimal
from werkzeug.security import check_password_hash, generate_password_hash
import time

app = Flask(__name__)
CORS(app)

# MongoDB connection
try:
    mongo_client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://mongodb-service:27017/'))
    mongo_db = mongo_client['financedb']
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Function to connect to MySQL
def connect_to_mysql(host, user, password, database):
    while True:
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print(f"Connected to MySQL ({database})")
            return connection
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL ({database}): {err}")
            time.sleep(5)  # Esperar 5 segundos antes de intentar nuevamente

# MySQL connection for financial data
mysql_conn_finances = connect_to_mysql(
    host=os.environ.get('MYSQL_HOST', 'mysql-finances'),
    user=os.environ.get('MYSQL_USER', 'root'),
    password=os.environ.get('MYSQL_PASSWORD', 'password'),
    database=os.environ.get('MYSQL_DATABASE', 'financedb')
)

# MySQL connection for user authentication
mysql_conn_users = connect_to_mysql(
    host=os.environ.get('MYSQL_USERDB_HOST', 'mysql-users'),
    user=os.environ.get('MYSQL_USERDB_USER', 'root'),
    password=os.environ.get('MYSQL_USERDB_PASSWORD', 'password'),
    database=os.environ.get('MYSQL_USERDB_DATABASE', 'userdb')
)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    print(f"Login attempt: username={username}, password={password}")
    
    while True:
        try:
            cursor = mysql_conn_users.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            break
        except mysql.connector.Error as err:
            print(f"Error querying MySQL (users): {err}")
            mysql_conn_users.reconnect(attempts=3, delay=5)
    
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
    
    while True:
        try:
            cursor = mysql_conn_users.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email)
            )
            mysql_conn_users.commit()
            cursor.close()
            break
        except mysql.connector.Error as err:
            print(f"Error inserting into MySQL (users): {err}")
            mysql_conn_users.reconnect(attempts=3, delay=5)
    
    return jsonify({"status": "success", "message": "User registered successfully"}), 201

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
    
    while True:
        try:
            cursor = mysql_conn_finances.cursor(dictionary=True)
            cursor.execute("SELECT * FROM finances")
            data = cursor.fetchall()
            cursor.close()
            break
        except mysql.connector.Error as err:
            print(f"Error querying MySQL (finances): {err}")
            mysql_conn_finances.reconnect(attempts=3, delay=5)
    
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

@app.route('/data/mysql', methods=['POST'])
def add_mysql_data():
    data = request.json
    date = data.get('date')
    expense = data.get('expense')
    revenue = data.get('revenue')
    
    print(f"Adding data to MySQL: date={date}, expense={expense}, revenue={revenue}")
    
    while True:
        try:
            cursor = mysql_conn_finances.cursor()
            cursor.execute(
                "INSERT INTO finances (date, expense, revenue) VALUES (%s, %s, %s)",
                (date, float(expense), float(revenue))
            )
            mysql_conn_finances.commit()
            cursor.close()
            break
        except mysql.connector.Error as err:
            print(f"Error inserting into MySQL (finances): {err}")
            mysql_conn_finances.reconnect(attempts=3, delay=5)
    
    return jsonify({"status": "success", "message": "Data added to MySQL"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)