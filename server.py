from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import json
import mysql.connector

app = Flask(__name__)

# Загрузка конфигурации из файла config.json
with open('config1.json') as config_file:
    config = json.load(config_file)

# Подключение к базе данных MySQL
db_connection = mysql.connector.connect(
    host=config['mysql_host'],
    user=config['mysql_user'],
    password=config['mysql_password'],
    database=config['mysql_database']
)
db_cursor = db_connection.cursor()

# Создание таблицы пользователей, если она не существует
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        login VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        registration_date DATETIME NOT NULL
    )
""")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    # Проверка наличия обязательных данных
    if not login or not password:
        return jsonify({'error': 'Missing login or password'}), 400

    # Проверка наличия пользователя в системе
    db_cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
    if db_cursor.fetchone():
        return jsonify({'error': 'User already exists'}), 400

    # Хеширование пароля
    password_hash = generate_password_hash(password)

    # Добавление пользователя в базу данных
    sql = "INSERT INTO users (login, password_hash, registration_date) VALUES (%s, %s, %s)"
    db_cursor.execute(sql, (login, password_hash, datetime.datetime.now()))
    db_connection.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    # Проверка наличия обязательных данных
    if not login or not password:
        return jsonify({'error': 'Missing login or password'}), 400

    # Проверка существования пользователя
    db_cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
    user = db_cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Проверка пароля
    if not check_password_hash(user[2], password):
        return jsonify({'error': 'Invalid password'}), 401

    return jsonify({'message': 'Login successful'}), 200

if __name__ == '__main__':
    # Включение поддержки HTTPS
    context = (config['ssl_certificate'], config['ssl_key'])
    app.run(debug=config['debug'], ssl_context=context)
