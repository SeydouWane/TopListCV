from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    rankers = db.relationship('CVRanker', backref='user', lazy=True)

class CVRanker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    skills = db.Column(db.Text)
    result_json = db.Column(db.Text)  # résultat enregistré (dict JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
