from nlp_engine import full_resume_analysis


def rank_resumes(resume_dict, job_description):

    results = []

    for name, text in resume_dict.items():
        analysis = full_resume_analysis(text, job_description)
        results.append((name, analysis["final_score"]))

    return sorted(results, key=lambda x: x[1], reverse=True)