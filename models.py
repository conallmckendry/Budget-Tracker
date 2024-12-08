from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):  
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    transactions = db.relationship('Transaction', backref='user', lazy=True)
    categories = db.relationship('Category', backref='user', lazy=True)

    def set_password(self, password):
        """Hash the password before saving it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password is correct."""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Flask-Login requires this method."""
        return str(self.id)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    transactions = db.relationship('Transaction', backref='category', lazy=True, cascade='all, delete-orphan')




