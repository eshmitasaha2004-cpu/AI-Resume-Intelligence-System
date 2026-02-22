import re
from collections import Counter

def preprocess(text):
    return re.findall(r'\b\w+\b', text.lower())


def calculate_match_score(resume_text, job_description):

    resume_words = preprocess(resume_text)
    job_words = preprocess(job_description)

    resume_set = set(resume_words)
    job_set = set(job_words)

    matched = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    base_score = int((len(matched) / len(job_set)) * 100) if job_set else 0

    # ATS Boost
    if len(resume_text) > 300:
        base_score = min(base_score + 5, 100)

    return base_score, matched, missing


def keyword_density(resume_text, job_description):
    resume_words = preprocess(resume_text)
    job_words = preprocess(job_description)

    match_count = sum(1 for word in resume_words if word in job_words)

    return round((match_count / len(resume_words)) * 100, 2) if resume_words else 0