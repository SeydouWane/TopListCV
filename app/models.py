from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    entreprise = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    rankers = db.relationship('CVRanker', backref='user', lazy=True)

class CVRanker(db.Model):
    __tablename__ = "ranker"  # clé pour que ForeignKey('ranker.id') fonctionne

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    skills = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fichier_paths = db.Column(db.PickleType)
    results = db.Column(db.PickleType)
    classement_mode = db.Column(db.String(50))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    cv_results = db.relationship("CVResult", backref="ranker", lazy=True)
          # Résultat du classement

class CVResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    relevance_score = db.Column(db.Float)
    experience_days = db.Column(db.Integer, default=0)  # 🆕
    ranker_id = db.Column(db.Integer, db.ForeignKey('ranker.id'))
