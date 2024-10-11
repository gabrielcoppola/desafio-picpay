from flask import jsonify
from flask_login import login_required

from . import main

@main.route('/protected')
@login_required
def protected():
    return jsonify(message="This is a protected route")