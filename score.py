def calculate_match_score(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    matched = resume_words.intersection(job_words)
    missing = job_words.difference(resume_words)

    if len(job_words) == 0:
        score = 0
    else:
        score = int((len(matched) / len(job_words)) * 100)

    return score, list(matched), list(missing)