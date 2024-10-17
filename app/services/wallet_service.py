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
    def transfer(user_id, target_email, amount):
        if amount <= 0:
            return None, "Transfer amount must be greater than zero"
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        wallet_target = db.session.query(Wallet).join(User).filter(User.email == target_email).first()
        if not wallet or not wallet_target:
            return None, "Wallet not found"
        if wallet.balance <= 0 or amount > wallet.balance:
            return None, "Insufficient balance"

        wallet.balance -= amount
        wallet_target.balance += amount

        balance_history = BalanceHistory(wallet_id=wallet.id_wallet, change_amount=-amount)
        balance_target_history = BalanceHistory(wallet_id=wallet_target.id_wallet, change_amount=+amount)
        db.session.add(balance_history)
        db.session.add(balance_target_history)
        db.session.commit()

        return wallet.balance, None

