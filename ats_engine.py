import re


def ats_score(resume_text):

    checks = {
        "Sufficient Length (>400 chars)": len(resume_text) > 400,
        "Contains Numbers (Quantified Results)": bool(re.search(r"\d+", resume_text)),
        "Contains Action Verbs": any(
            word in resume_text.lower()
            for word in [
                "developed", "built", "designed",
                "implemented", "engineered",
                "optimized", "led", "created",
                "improved", "achieved"
            ]
        ),
        "Has Experience Section": "experience" in resume_text.lower(),
        "Has Skills Section": "skills" in resume_text.lower(),
        "Has Education Section": "education" in resume_text.lower(),
    }

    score = int((sum(checks.values()) / len(checks)) * 100)

    return score, checks