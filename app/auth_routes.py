from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        entreprise = request.form['entreprise']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email déjà utilisé.')
            return redirect(url_for('auth.register'))

        new_user = User(
            nom=nom, prenom=prenom, entreprise=entreprise,
            email=email, password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie. Vous pouvez vous connecter.")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))

        flash("Email ou mot de passe invalide.")
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
