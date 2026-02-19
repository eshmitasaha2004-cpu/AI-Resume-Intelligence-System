from openai import OpenAI
import os

def rewrite_resume(resume_text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    Improve the following resume to make it more professional,
    impactful, and ATS-friendly. Use strong action verbs.

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional resume expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
