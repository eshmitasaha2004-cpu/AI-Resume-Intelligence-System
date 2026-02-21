import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


def extract_top_keywords(text, top_n=15):
    """
    Extract top TF-IDF keywords from given text.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_array = np.array(vectorizer.get_feature_names_out())
    tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]

    top_keywords = feature_array[tfidf_sorting][:top_n]
    return set(top_keywords)


def calculate_match_score(resume_text, job_description):
    """
    Returns:
    - similarity score
    - matched skills
    - missing skills
    """

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    # TF-IDF similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = round(float(similarity[0][0]) * 100, 2)

    # Extract top keywords from job description
    job_keywords = extract_top_keywords(job_description, top_n=20)

    # Resume word set
    resume_words = set(resume_text.split())

    matched_skills = job_keywords.intersection(resume_words)
    missing_skills = job_keywords.difference(resume_words)

    return score, list(matched_skills), list(missing_skills)