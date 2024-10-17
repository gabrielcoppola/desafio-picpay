from flask import request, jsonify
from flask_login import login_required

from app.middleware.auth_middleware import token_required
from app.services.wallet_service import WalletService

from . import main

@main.route('/protected')
@token_required
def protected(current_user):
    return jsonify(message="This is a protected route", user=current_user.email)

@main.route('/wallet/balance', methods=['GET'])
@token_required
def get_wallet_balance(current_user):
    balance, error = WalletService.get_wallet_balance(current_user.id_user)
    if error:
        return jsonify(error=error), 400
    return jsonify(balance=balance), 200

@main.route('/wallet/deposit', methods=['POST'])
@token_required
def deposit(current_user):
    data = request.get_json()
    amount = data.get('amount')

    balance, error = WalletService.deposit(current_user.id_user, amount)

    if amount is None:
        response = {
            "status": "error",
            "data": None,
            "error": {
                "code": 400,
                "message": "Amount is required"
            }
        }
        return jsonify(response), 400

    if error:
        response = {
            "status": "error",
            "data": None,
            "error": {
                "code": 400,
                "message": error
            }
        }
        return jsonify(response), 400

    response = {
        "status": "success",
        "data": {
            "balance": balance,
            "message": "Deposit successful"
        },
        "error": None
    }
    return jsonify(response), 200

@main.route('/wallet/transfer', methods=['POST'])
@token_required
def transfer(current_user):
    data = request.get_json()

    amount = data.get('amount')
    target_wallet = data.get('transfer_to')

    balance, error = WalletService.transfer(current_user.id_user, target_wallet, amount)

    if amount is None:
        response = {
            "status": "error",
            "data": None,
            "error": {
                "code": 400,
                "message": "Amount is required"
            }
        }
        return jsonify(response), 400

    if error:
        response = {
            "status": "error",
            "data": None,
            "error": {
                "code": 400,
                "message": error
            }
        }
        return jsonify(response), 400

    response = {
        "status": "success",
        "data": {
            "balance": balance,
            "message": "Deposit successful"
        },
        "error": None
    }
    return jsonify(response), 200


# @main.route('/protected')
# @login_required
# def protected():
#     return jsonify(message="This is a protected route")