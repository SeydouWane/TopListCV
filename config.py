import os

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Qqmkl%408345@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Dossier pour stocker les CV PDF uploadés temporairement
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
