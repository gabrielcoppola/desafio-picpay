from flask import request, jsonify
from flask_login import login_user, logout_user, login_required

from . import auth
from .. import db
from app.models.user import User
from app.models.wallet import Wallet
from utils.jwt_utils import generate_token
from app.common.enums import UserType

def validate_fields(data, required_fields):
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"
    return True, None

def validate_uniqueness(model, data, unique_fields):
    for field in unique_fields:
        if model.query.filter_by(**{field: data.get(field)}).first():
            return False, f"{field.replace('_', ' ').title()} already exists"
    return True, None

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['full_name', 'user_type', 'email', 'tax_id', 'password']
    unique_fields = ['email', 'tax_id']

    # Route level validation
    try:
        user_type = UserType(data.get('user_type').lower())
    except ValueError:
        return jsonify({'error': 'Invalid user type'}), 400

    is_valid, error_message = validate_fields(data, required_fields)
    if not is_valid:
        return jsonify(message=error_message), 400

    is_unique, error_message = validate_uniqueness(User, data, unique_fields)
    if not is_unique:
        return jsonify(message=error_message), 400

    new_user = User(
        full_name=data.get('full_name'),
        user_type=data.get('user_type').lower(),
        email=data.get('email'),
        tax_id=data.get('tax_id')
    )

    try:
        new_user.set_password(data.get('password'))
        new_user.validate_user_type(data.get('user_type').lower())
        db.session.add(new_user)
        db.session.commit()

        wallet = Wallet(user_id=new_user.id_user, balance=0.00)
        db.session.add(wallet)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        token = generate_token(user.id_user)
        return jsonify(token=token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message="Logout successful"), 200