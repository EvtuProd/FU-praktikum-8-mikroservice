from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)

# Хранилище пользователей (в реальном приложении лучше использовать базу данных)
users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    # Проверка наличия обязательных данных
    if not login or not password:
        return jsonify({'error': 'Missing login or password'}), 400

    # Проверка наличия пользователя в системе
    if login in users:
        return jsonify({'error': 'User already exists'}), 400

    # Хеширование пароля
    password_hash = generate_password_hash(password)

    # Добавление пользователя в хранилище
    users[login] = {
        'password_hash': password_hash,
        'registration_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

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
    if login not in users:
        return jsonify({'error': 'User not found'}), 404

    # Проверка пароля
    if not check_password_hash(users[login]['password_hash'], password):
        return jsonify({'error': 'Invalid password'}), 401

    return jsonify({'message': 'Login successful'}), 200

if __name__ == '__main__':
    # Включение поддержки HTTPS
    context = ('ssl.crt', 'ssl.key')  # Пути к сертификату и ключу
    app.run(debug=True, ssl_context=context)
