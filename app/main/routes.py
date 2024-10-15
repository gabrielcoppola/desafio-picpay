from flask import jsonify
from flask_login import login_required

from app.middleware.auth_middleware import token_required

from . import main

@main.route('/protected')
@token_required
def protected(current_user):
    return jsonify(message="This is a protected route", user=current_user.email)

# @main.route('/protected')
# @login_required
# def protected():
#     return jsonify(message="This is a protected route")