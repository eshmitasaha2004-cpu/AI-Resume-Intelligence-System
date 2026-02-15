import streamlit as st
import PyPDF2
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Intelligence SaaS", layout="centered")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# LOGIN PAGE
# -----------------------------
if not st.session_state.logged_in:

    st.title("🔐 Login - AI Resume Intelligence")

    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Your Email")

    if st.button("Login"):
        if name and email:
            st.session_state.logged_in = True
            st.session_state.user = name
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Please enter both name and email.")

# -----------------------------
# MAIN DASHBOARD
# -----------------------------
else:

    st.title(f"🧠 Welcome, {st.session_state.user}")
    st.markdown("### AI Resume Intelligence Dashboard")
    st.markdown("---")

    # -----------------------------
    # PDF EXTRACTION
    # -----------------------------
    def extract_text_from_pdf(file):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        return text

    def calculate_similarity(text1, text2):
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return similarity

    # -----------------------------
    # INPUT SECTION
    # -----------------------------
    st.header("📄 Resume Input")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    resume_text_input = st.text_area("OR Paste Resume Text")

    resume_text = ""

    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
    elif resume_text_input:
        resume_text = resume_text_input

    st.header("💼 Job Description")
    job_description = st.text_area("Paste Job Description")

    # -----------------------------
    # ANALYSIS
    # -----------------------------
    if st.button("🔍 Analyze Resume"):

        if resume_text and job_description:

            resume_clean = clean_text(resume_text)
            job_clean = clean_text(job_description)

            similarity = calculate_similarity(resume_clean, job_clean)
            match_percentage = round(similarity * 100, 2)

            st.subheader("📊 Match Score")
            st.progress(int(match_percentage))
            st.success(f"{match_percentage}% Match")

            # Save history
            st.session_state.history.append(match_percentage)

        else:
            st.error("Please upload/paste resume and job description.")

    # -----------------------------
    # HISTORY SECTION
    # -----------------------------
    if st.session_state.history:
        st.markdown("---")
        st.subheader("📈 Analysis History")

        history_df = pd.DataFrame({
            "Attempt": range(1, len(st.session_state.history) + 1),
            "Match %": st.session_state.history
        })

        st.dataframe(history_df)

    # -----------------------------
    # LOGOUT
    # -----------------------------
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.history = []
        st.rerun()

    # -----------------------------
    # FOOTER
    # -----------------------------
    st.markdown("---")
    st.markdown("<div style='text-align:center;'>Developed by <b>Eshmita Saha</b> 💻</div>", unsafe_allow_html=True)
