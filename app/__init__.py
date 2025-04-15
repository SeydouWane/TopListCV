from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth_routes import auth
    from .main_routes import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
