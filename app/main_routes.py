from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory
from flask_login import login_required, current_user
from .models import db, CVRanker, CVResult
from .utils import extract_text_from_pdf_bytes, extract_experience_duration, compute_relevance
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

# Accueil
@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

# Tableau de bord
@main.route('/dashboard')
@login_required
def dashboard():
    rankers = CVRanker.query.filter_by(user_id=current_user.id).order_by(CVRanker.date_creation.desc()).all()
    return render_template('dashboard.html', rankers=rankers)

# Créer un nouveau CV Ranker
@main.route('/ranker/create', methods=['GET', 'POST'])
@login_required
def create_ranker():
    if request.method == 'POST':
        titre = request.form['titre']
        skills = request.form['skills']
        mode = request.form.get('mode', 'both')  # 👈 récupération du mode (skills / experience / both)
        files = request.files.getlist('cv_files')

        folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(folder, exist_ok=True)

        saved_files = []

        # Création du Ranker vide pour obtenir son ID
        new_ranker = CVRanker(
            titre=titre,
            skills=skills,
            user_id=current_user.id,
            fichier_paths=[],
            results={},
            classement_mode=mode
        )
        db.session.add(new_ranker)
        db.session.flush()  # Permet d’avoir new_ranker.id sans commit

        for f in files:
            if f.filename.lower().endswith('.pdf'):
                filename = secure_filename(f.filename)
                filepath = os.path.join(folder, filename)
                f.save(filepath)
                saved_files.append(filename)

                with open(filepath, "rb") as doc:
                    text = extract_text_from_pdf_bytes(doc.read())
                    score = compute_relevance(text, skills)
                    experience = extract_experience_duration(text)

                    # Calcul du score combiné si besoin
                    if mode == "skills":
                        final_score = score
                    elif mode == "experience":
                        final_score = experience
                    elif mode == "both":
                        final_score = round(0.7 * score + 0.3 * (experience / 365), 4)
                    else:
                        final_score = score

                    result = CVResult(
                        filename=filename,
                        relevance_score=score,
                        experience_days=experience,
                        ranker_id=new_ranker.id
                    )
                    db.session.add(result)

        new_ranker.fichier_paths = saved_files
        db.session.commit()

        return redirect(url_for('main.view_ranker', ranker_id=new_ranker.id))

    return render_template('create_ranker.html')

# Voir un Ranker avec tri
@main.route("/ranker/view/<int:ranker_id>")
@login_required
def view_ranker(ranker_id):
    ranker = CVRanker.query.get_or_404(ranker_id)
    tri = request.args.get("tri", "competences")

    results = CVResult.query.filter_by(ranker_id=ranker.id).all()

    if tri == "competences":
        results.sort(key=lambda r: r.relevance_score or 0, reverse=True)
    elif tri == "experience":
        results.sort(key=lambda r: r.experience_days or 0, reverse=True)
    elif tri == "combine":
        results.sort(key=lambda r: 0.7 * (r.relevance_score or 0) + 0.3 * ((r.experience_days or 0) / 365), reverse=True)

    return render_template("view_ranker.html", ranker=ranker, results=results)

# Voir un fichier PDF
@main.route('/uploads/<filename>')
@login_required
def serve_uploaded_file(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)

# Supprimer un CV Ranker
@main.route('/ranker/delete/<int:ranker_id>', methods=['POST'])
@login_required
def delete_ranker(ranker_id):
    ranker = CVRanker.query.filter_by(id=ranker_id, user_id=current_user.id).first_or_404()
    CVResult.query.filter_by(ranker_id=ranker.id).delete()
    db.session.delete(ranker)
    db.session.commit()
    return redirect(url_for('main.dashboard'))
