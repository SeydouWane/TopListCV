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
