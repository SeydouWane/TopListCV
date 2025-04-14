from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    from .routes import main
    app.register_blueprint(main)

    return app
