from flask_login import UserMixin
from src.web_app.app_config import db
import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')
    text = db.Column(db.String(500), nullable=False)
    mushroom_id = db.Column(
        db.Integer,
        db.ForeignKey('mushroom.id'),
        nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)


class Mushroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    species = db.Column(db.String(120), nullable=False)
    odds = db.Column(db.Integer, nullable=False)
    comments = db.relationship('Comment', backref='mushroom', lazy=True)
