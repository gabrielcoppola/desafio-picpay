from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.common.enums import UserType

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.Enum(UserType), nullable=False, default=UserType.USER)
    full_name = db.Column(db.String(255), unique=False, nullable=False)
    tax_id = db.Column(db.String(20), unique=True, nullable=False)  # Flexibilidade para identificadores internacionais
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    wallet = db.relationship('Wallet', backref='owner', uselist=False, lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_user_type(self, user_type):
        self.user_type = UserType(user_type)
        if not isinstance(self.user_type, UserType):
            raise ValueError(f'Invalid user type: {self.user_type}')

    def __repr__(self):
        return f'<User {self.email}>'