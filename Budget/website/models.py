from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func


class Transaction(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    amount = db.Column(db.Float(2), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False, default="income")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, amount, date, title, type, user_id):
        self.amount = amount
        self.date = date
        self.title = title
        self.user_id = user_id
        self.type = type


class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    transaction = db.relationship("Transaction")

    def __init__(self, email, username, first_name, last_name, password):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
