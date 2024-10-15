from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), unique=False, nullable=False)
    tax_id = db.Column(db.String(20), unique=True, nullable=False)  # Flexibilidade para identificadores internacionais
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    wallet = db.relationship('Wallet', backref='owner', uselist=False, lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

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