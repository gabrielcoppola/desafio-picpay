from .. import db

class Wallet(db.Model):
    __tablename__ = 'wallet'

    id_wallet = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    balance_history = db.relationship('BalanceHistory', backref='wallet', lazy=True)

    def __repr__(self):
        return f'<Wallet {self.id_wallet}>'

class BalanceHistory(db.Model):
    __tablename__ = 'balance_history'

    id_history = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id_wallet'), nullable=False)
    change_amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<BalanceHistory {self.id_history} - {self.change_amount}>'