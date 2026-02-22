from scorer import calculate_match_score

def rank_resumes(resume_texts, job_description):

    results = []

    for name, text in resume_texts.items():
        score, _, _ = calculate_match_score(text, job_description)
        results.append((name, score))

    results.sort(key=lambda x: x[1], reverse=True)

    return results