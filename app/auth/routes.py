from flask import request, jsonify
from flask_login import login_user

from . import auth
from ..models import users

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = next((u for u in users.values() if u.username == username and u.password == password), None)

    if user:
        login_user(user)
        return jsonify(message="Login successful"), 200
    else:
        return jsonify(message="Invalid credentials"), 401