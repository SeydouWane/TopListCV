## 📝 Rapport du Projet : CV Smart Ranker

### 🔖 Titre :  
**Développement d’une plateforme intelligente de tri et de classement de CV par compétences et expériences professionnelles**

---

### 🎯 Objectif du projet

Ce projet a pour objectif de **faciliter le processus de recrutement** en automatisant le classement des CV soumis à une offre d'emploi, à partir :
- des **compétences recherchées**
- du **niveau d’expérience professionnelle détecté**
- ou une **combinaison pondérée des deux**

---

### 🧱 Stack Technologique

| Composant     | Détail                         |
|---------------|--------------------------------|
| **Backend**   | Flask (Python)                 |
| **NLP**       | spaCy (`en_core_web_md`)       |
| **Base de données** | PostgreSQL avec SQLAlchemy ORM |
| **Frontend**  | HTML + CSS + Jinja2            |
| **Extraction PDF** | PyPDF2                   |
| **Stockage fichiers** | `uploads/` en local         |

---

### 📁 Architecture du projet

```
cv-projet/
│
├── app/
│   ├── __init__.py               # Configuration Flask
│   ├── models.py                # Modèles SQLAlchemy : CVRanker, CVResult, User
│   ├── utils.py                 # NLP : extraction texte, score, expérience
│   ├── auth_routes.py           # Authentification : login / register
│   ├── main_routes.py           # Routes CV Ranker
│   ├── templates/               # Templates HTML
│   └── static/                  # Fichiers CSS
│
├── run.py                       # Lancement Flask
├── requirements.txt             # Dépendances
└── config.py                    # Config (DB URI, upload folder, secret key)
```

---

### 👤 Gestion des utilisateurs

Chaque utilisateur peut :
- s’inscrire avec : **nom, prénom, entreprise, email pro, mot de passe**
- se connecter via login sécurisé
- créer plusieurs projets de **CV Rankers**
- supprimer ses rankers
- voir les résultats avec tri

---

### 📥 Création d’un CV Ranker

L’utilisateur fournit :
- un **nom d’appel à candidature**
- un ou plusieurs **fichiers PDF** (en sélectionnant un dossier entier)
- une **liste de compétences**
- un **mode de classement** :
  - `Compétences`
  - `Expérience`
  - `Compétences + Expérience`

---

### 🧠 Fonctionnement NLP

1. **Extraction du texte** depuis le PDF avec `PyPDF2`
2. **Matching des compétences** par similarité sémantique (spaCy) :
   - +1.5 si mot-clé exact
   - +similitude sémantique sinon
3. **Détection de l’expérience** via expressions régulières :
   - `2 ans`, `6 mois`, `15 jours` → convertis en **jours d’expérience**

---

### 📊 Affichage des résultats

Pour chaque CV :
- Affichage du **score de pertinence**
- Nombre de **jours d’expérience**
- Lien pour **voir le CV**
- Tri dynamique selon :
  - score de pertinence (`skills`)
  - expérience (`experience`)
  - score combiné (`0.7*skills + 0.3*exp_en_années`)

---

### 🧪 Exemple d'entrée utilisateur

| Appel à candidature | Compétences       | Mode       |
|---------------------|-------------------|------------|
| Data Scientist      | Python, SQL, ML   | Combine    |

---

### ✅ Fonctionnalités principales

- ✅ Authentification sécurisée
- ✅ Upload multiple de fichiers (dossier complet)
- ✅ Extraction automatique de contenu PDF
- ✅ Analyse NLP intelligente
- ✅ Détection d’expérience professionnelle
- ✅ Sauvegarde en base PostgreSQL
- ✅ Interface Dashboard avec vue et suppression
- ✅ Tri dynamique des résultats

---

### 🗂 Modèle de base de données

#### `User`
```python
id, nom, prenom, entreprise, email, password
```

#### `CVRanker`
```python
id, titre, skills, user_id (foreign key), fichier_paths (JSON), date_creation
```

#### `CVResult`
```python
id, filename, relevance_score, experience_days, ranker_id (foreign key)
```

---

### 🧠 Conclusion

Ce projet propose une solution concrète à l’automatisation du **tri de CV** en combinant des techniques de **traitement automatique du langage naturel** et une interface web simple à utiliser. Il rend le **recrutement plus rapide et objectif**, en réduisant la charge humaine liée à l’analyse manuelle des candidatures.
