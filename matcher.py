import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    """
    Basic text cleaning:
    - Lowercasing
    - Removing special characters
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


def calculate_match_score(resume_text, job_description):
    """
    Calculates similarity score between resume and job description
    using TF-IDF + Cosine Similarity.
    """

    # Clean both texts
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])

    # Compute cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Convert to percentage
    score = round(float(similarity[0][0]) * 100, 2)

    return score