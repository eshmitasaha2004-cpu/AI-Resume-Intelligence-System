import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------------------------------
# TEXT CLEANING
# -----------------------------------------------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------------------------------
# SECTION DETECTION
# -----------------------------------------------------
def detect_sections(text):

    sections = {
        "experience": False,
        "education": False,
        "skills": False,
        "projects": False,
    }

    text = preprocess(text)

    for section in sections.keys():
        if section in text:
            sections[section] = True

    return sections


# -----------------------------------------------------
# ACTION VERB SCORING
# -----------------------------------------------------
def action_verb_score(text):

    action_verbs = [
        "developed", "built", "designed",
        "implemented", "engineered",
        "optimized", "led", "created",
        "improved", "achieved"
    ]

    text = preprocess(text)

    count = sum(text.count(verb) for verb in action_verbs)

    return min(count * 5, 25)  # max 25 points


# -----------------------------------------------------
# QUANTIFICATION SCORING
# -----------------------------------------------------
def quantification_score(text):

    numbers = re.findall(r"\d+", text)

    return min(len(numbers) * 3, 20)  # max 20 points


# -----------------------------------------------------
# SKILL EXTRACTION
# -----------------------------------------------------
def extract_skills(text):

    skill_bank = [
        "python", "java", "c++", "javascript",
        "machine learning", "deep learning",
        "nlp", "pandas", "numpy",
        "tensorflow", "pytorch",
        "flask", "django", "react",
        "node", "sql", "mysql",
        "mongodb", "aws", "docker",
        "kubernetes", "git", "linux",
        "rest api", "microservices"
    ]

    text = preprocess(text)

    return sorted(
        list(set(skill for skill in skill_bank if skill in text))
    )


# -----------------------------------------------------
# SKILL MATCH SCORING
# -----------------------------------------------------
def skill_match_score(resume_text, job_text):

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))

    if len(job_skills) == 0:
        return 0, [], []

    matched = resume_skills.intersection(job_skills)
    missing = job_skills.difference(resume_skills)

    score = int((len(matched) / len(job_skills)) * 100)

    return score, sorted(list(matched)), sorted(list(missing))


# -----------------------------------------------------
# SEMANTIC SIMILARITY (TF-IDF)
# -----------------------------------------------------
def semantic_similarity(resume_text, job_text):

    resume_text = preprocess(resume_text)
    job_text = preprocess(job_text)

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_text])

    similarity = cosine_similarity(
        vectors[0:1], vectors[1:2]
    )[0][0]

    return int(similarity * 100)


# -----------------------------------------------------
# KEYWORD DENSITY
# -----------------------------------------------------
def keyword_density(text, top_n=10):

    text = preprocess(text)
    words = text.split()

    freq = {}

    for word in words:
        if len(word) > 3:
            freq[word] = freq.get(word, 0) + 1

    sorted_freq = sorted(
        freq.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_freq[:top_n]


# -----------------------------------------------------
# FINAL HYBRID SCORING ENGINE
# -----------------------------------------------------
def full_resume_analysis(resume_text, job_text):

    # Core signals
    semantic_score = semantic_similarity(resume_text, job_text)
    skill_score, matched_skills, missing_skills = skill_match_score(
        resume_text, job_text
    )

    action_score = action_verb_score(resume_text)
    quant_score = quantification_score(resume_text)

    sections = detect_sections(resume_text)
    section_score = sum(sections.values()) * 5  # max 20

    # Weighted final score
    final_score = int(
        0.4 * semantic_score +
        0.3 * skill_score +
        0.1 * action_score +
        0.1 * quant_score +
        0.1 * section_score
    )

    return {
        "final_score": final_score,
        "semantic_score": semantic_score,
        "skill_score": skill_score,
        "action_score": action_score,
        "quant_score": quant_score,
        "section_score": section_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "sections_detected": sections,
        "resume_keywords": keyword_density(resume_text),
        "job_keywords": keyword_density(job_text),
    }