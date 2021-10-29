from flask_login import UserMixin
from . import db
import datetime


class User(UserMixin, db.Model):
    def get_id(self):
        return self.email

    __tablename__ = 'users'
    email = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text)
    name = db.Column(db.Text)
    contact = db.Column(db.Text)
    address = db.Column(db.Text)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    desc = db.Column(db.Text)
    type = db.Column(db.Text)
    image_path = db.Column(db.Text)
    ticket_all = db.Column(db.Integer, default=100)
    ticket_sold = db.Column(db.Integer, default=0)
    ticket_price = db.Column(db.Float, default=80)
    date = db.Column(db.DateTime)
    status = db.Column(db.Text)
    created = db.Column(db.Text, db.ForeignKey('users.email'))


class Receipt(db.Model):
    __tablename__ = 'user_receipts'
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.Integer)
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_user = db.Column(db.Text, db.ForeignKey('users.email'))
    created = db.Column(db.DateTime, default=datetime.datetime.now)


class Comment(db.Model):
    __tablename__ = 'user_comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_user = db.Column(db.Text, db.ForeignKey('users.email'))
    created = db.Column(db.DateTime, default=datetime.datetime.now)
