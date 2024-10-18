import requests

from app import db
from app.models.wallet import Wallet, BalanceHistory
from app.models.user import User

class WalletService:
    @staticmethod
    def get_wallet_balance(user_id):
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if wallet:
            return wallet.balance, None
        else:
            return None, "Wallet not found"

    @staticmethod
    def deposit(user_id, amount):
        if amount <= 0:
            return None, "Deposit amount must be greater than zero"

        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            return None, "Wallet not found"
        if wallet.balance <= 0:
            return None, "Wallet balance must be greater than zero"

        wallet.balance += amount
        balance_history = BalanceHistory(wallet_id=wallet.id_wallet, change_amount=amount)
        db.session.add(balance_history)
        db.session.commit()

        return wallet.balance, None

    @staticmethod
    def _get_wallets(user_id, target_email):
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        wallet_target = db.session.query(Wallet).join(User).filter(User.email == target_email).first()
        if not wallet or not wallet_target:
            return None, None, "Wallet not found"
        return wallet, wallet_target, None

    @staticmethod
    def _authorize_transfer():
        url = "https://util.devi.tools/api/v2/authorize"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('data', {}).get('authorization', False), None
        return None, "Authorization service error"

    @staticmethod
    def _perform_transfer(wallet, wallet_target, amount):
        wallet.balance -= amount
        wallet_target.balance += amount

        balance_history = BalanceHistory(wallet_id=wallet.id_wallet, change_amount=-amount)
        balance_target_history = BalanceHistory(wallet_id=wallet_target.id_wallet, change_amount=amount)
        db.session.add(balance_history)
        db.session.add(balance_target_history)
        db.session.commit()

    @staticmethod
    def transfer(user_id, target_email, amount):
        if amount <= 0:
            return None, "Transfer amount must be greater than zero"

        wallet, wallet_target, error = WalletService._get_wallets(user_id, target_email)
        if error:
            return None, error

        if wallet.balance < amount:
            return None, "Insufficient balance"

        authorization_status, error = WalletService._authorize_transfer()
        if error or not authorization_status:
            return None, "Authorization failed"

        WalletService._perform_transfer(wallet, wallet_target, amount)
        return wallet.balance, None