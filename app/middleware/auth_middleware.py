from functools import wraps
from flask import request, jsonify

from utils.jwt_utils import decode_token
from ..models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()
        if not token:
            return jsonify(message='Token is missing'), 401
        data = decode_token(token)
        if data is None:
            return jsonify(message='Token is invalid or expired'), 401
        current_user = User.query.get(data['user_id'])
        return f(current_user, *args, **kwargs)
    return decorated