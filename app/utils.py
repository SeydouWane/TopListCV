import spacy
import PyPDF2
from io import BytesIO

nlp = spacy.load("en_core_web_md")

def extract_text_from_pdf_bytes(content_bytes):
    text = ""
    try:
        pdf_file = BytesIO(content_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text.lower()
    except Exception as e:
        print("Erreur PDF :", e)
    return text

def rank_cvs_by_skills(cvs, skills_input):
    skill_list = [s.strip().lower() for s in skills_input.split(",")]
    skill_vecs = [nlp(skill) for skill in skill_list]

    results = []
    for filename, content in cvs.items():
        content_doc = nlp(content)
        score = 0
        for skill, vec in zip(skill_list, skill_vecs):
            if skill in content:
                score += 1.5
            sim_scores = [token.similarity(vec) for token in content_doc if token.has_vector and not token.is_stop]
            score += max(sim_scores) if sim_scores else 0
        results.append((filename, round(score, 4)))
    return sorted(results, key=lambda x: x[1], reverse=True)


import re

import re

def extract_experience_duration(text):
    # Matches format: "2 ans", "3 an", "4 mois", "10 jours"
    year_matches = re.findall(r'(\d+)\s?(?:ans|an)', text, re.IGNORECASE)
    month_matches = re.findall(r'(\d+)\s?mois', text, re.IGNORECASE)
    day_matches = re.findall(r'(\d+)\s?(?:jour|jours)', text, re.IGNORECASE)

    total_days = 0

    for val in year_matches:
        total_days += int(val) * 365
    for val in month_matches:
        total_days += int(val) * 30
    for val in day_matches:
        total_days += int(val)

    return total_days


def rank_cvs_with_mode(cvs, skills_input, mode="both"):
    """
    Classe les CV selon :
    - 'skills' : score de pertinence uniquement
    - 'experience' : durée d'expérience estimée
    - 'both' : score combiné (pondération 0.7 / 0.3)
    """
    skill_list = [s.strip().lower() for s in skills_input.split(",")]
    skill_vecs = [nlp(skill) for skill in skill_list]

    scored_cvs = []

    for filename, content in cvs.items():
        doc = nlp(content)

        # Score de pertinence
        score = 0
        for skill, vec in zip(skill_list, skill_vecs):
            if skill in content:
                score += 1.5
            sim_scores = [token.similarity(vec) for token in doc if token.has_vector and not token.is_stop]
            score += max(sim_scores) if sim_scores else 0

        # Score d’expérience
        experience_days = extract_experience_duration(content)

        # Score final selon le mode choisi
        if mode == "skills":
            final_score = round(score, 4)
        elif mode == "experience":
            final_score = experience_days
        elif mode == "both":
            final_score = round(0.7 * score + 0.3 * (experience_days / 365), 4)
        else:
            final_score = round(score, 4)

        scored_cvs.append((filename, final_score, experience_days))

    # Tri
    scored_cvs.sort(key=lambda x: x[1], reverse=True)
    return scored_cvs

def compute_relevance(text, skills_input):
    doc = nlp(text)
    skill_list = [s.strip().lower() for s in skills_input.split(",")]
    skill_vecs = [nlp(skill) for skill in skill_list]

    score = 0
    for skill, vec in zip(skill_list, skill_vecs):
        if skill in text:
            score += 1.5
        sim_scores = [token.similarity(vec) for token in doc if token.has_vector and not token.is_stop]
        score += max(sim_scores) if sim_scores else 0

    return round(score, 4)
