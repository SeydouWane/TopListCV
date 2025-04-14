from flask import Blueprint, render_template, request, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
from .utils import extract_text_from_pdf_bytes, rank_cvs_by_skills

main = Blueprint("main", __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        skills = request.form.get('skills')
        files = request.files.getlist('cv_files')
        uploads_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(uploads_folder, exist_ok=True)

        cvs = {}
        for f in files:
            if f.filename.lower().endswith('.pdf'):
                filename = secure_filename(f.filename)
                save_path = os.path.join(uploads_folder, filename)
                f.save(save_path)

                with open(save_path, "rb") as pdf_file:
                    content = pdf_file.read()
                    text = extract_text_from_pdf_bytes(content)
                    cvs[filename] = text

        results = rank_cvs_by_skills(cvs, skills)
        return render_template("result.html", results=results, skills=skills)

    return render_template("index.html")

# Nouveau route : pour afficher ou télécharger un CV
@main.route('/cv/<filename>')
def serve_cv(filename):
    uploads_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(uploads_folder, filename)
