import streamlit as st
import hashlib
from datetime import datetime
import pandas as pd

from utils import extract_text_from_pdf
from database import (
    init_db,
    create_user,
    verify_user,
    insert_history,
    get_user_history,
    get_all_history,
)
from nlp_engine import full_resume_analysis
from ml_engine import predict_hiring_probability
from recruiter import rank_resumes


# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(page_title="AI Resume Intelligence", layout="wide")
init_db()


# -------------------------------------------------
# PASSWORD HASH
# -------------------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()


# -------------------------------------------------
# SESSION INIT
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# -------------------------------------------------
# AUTHENTICATION
# -------------------------------------------------
if not st.session_state.logged_in:

    st.title("🔐 AI Resume Intelligence Platform")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if verify_user(username, hash_password(password)):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("Choose Username", key="signup_user")
        new_pass = st.text_input("Choose Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            if len(new_pass) < 6:
                st.warning("Password must be at least 6 characters")
            else:
                if create_user(new_user, hash_password(new_pass)):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username already exists")

    st.stop()


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title(f"👤 {st.session_state.user}")

page = st.sidebar.radio(
    "Navigation",
    [
        "Resume Analyzer",
        "Dashboard",
        "Leaderboard",
        "Recruiter Panel",
    ],
)

st.sidebar.button("Logout", on_click=logout)


# -------------------------------------------------
# RESUME ANALYZER
# -------------------------------------------------
if page == "Resume Analyzer":

    st.title("📄 AI Resume Analyzer")

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        resume_text_input = st.text_area("Or Paste Resume Text")

    with col2:
        job_description = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):

        resume_text = (
            extract_text_from_pdf(uploaded_file)
            if uploaded_file
            else resume_text_input
        )

        if resume_text and job_description:

            analysis = full_resume_analysis(resume_text, job_description)

            ml_probability = predict_hiring_probability(analysis)

            st.subheader("🎯 AI Hiring Prediction")
            st.metric("Predicted Hiring Probability", f"{ml_probability}%")
            st.progress(ml_probability / 100)

            if ml_probability > 75:
                st.success("High likelihood of selection")
            elif ml_probability > 50:
                st.warning("Moderate hiring probability")
            else:
                st.error("Low hiring probability")

            st.divider()

            st.subheader("📊 Feature Breakdown")

            st.write(f"Semantic Score: {analysis['semantic_score']}%")
            st.write(f"Skill Match Score: {analysis['skill_score']}%")
            st.write(f"Action Verb Score: {analysis['action_score']}")
            st.write(f"Quantification Score: {analysis['quant_score']}")
            st.write(f"Section Completeness Score: {analysis['section_score']}")

            st.divider()

            st.subheader("✅ Matched Skills")
            st.write(analysis["matched_skills"])

            st.subheader("❌ Missing Skills")
            st.write(analysis["missing_skills"])

            st.subheader("📌 Resume Keywords")
            st.write(analysis["resume_keywords"])

            # Save history
            insert_history(
                st.session_state.user,
                ml_probability,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

        else:
            st.warning("Please provide resume and job description.")


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
elif page == "Dashboard":

    st.title("📊 Personal Dashboard")

    df = get_user_history(st.session_state.user)

    if not df.empty:

        total = len(df)
        avg_score = int(df["score"].mean())
        best_score = int(df["score"].max())

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Analyses", total)
        col2.metric("Average Hiring Probability", f"{avg_score}%")
        col3.metric("Best Probability", f"{best_score}%")

        st.subheader("Performance Trend")
        st.line_chart(df.set_index("date")["score"])

    else:
        st.info("No analysis history yet.")


# -------------------------------------------------
# LEADERBOARD
# -------------------------------------------------
elif page == "Leaderboard":

    st.title("🏆 Global Leaderboard")

    df = get_all_history()

    if not df.empty:

        leaderboard = (
            df.groupby("user")["score"]
            .max()
            .reset_index()
            .sort_values(by="score", ascending=False)
        )

        leaderboard["Rank"] = range(1, len(leaderboard) + 1)

        st.dataframe(
            leaderboard[["Rank", "user", "score"]],
            use_container_width=True,
        )

    else:
        st.info("No leaderboard data available.")


# -------------------------------------------------
# RECRUITER PANEL
# -------------------------------------------------
elif page == "Recruiter Panel":

    st.title("🏢 Recruiter Multi-Resume Ranking")

    job_description = st.text_area("Paste Job Description")
    uploaded_files = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("Rank Candidates") and job_description and uploaded_files:

        resume_dict = {}

        for file in uploaded_files:
            resume_dict[file.name] = extract_text_from_pdf(file)

        ranked_results = rank_resumes(resume_dict, job_description)

        st.subheader("📊 Candidate Ranking")

        for rank, (name, score) in enumerate(ranked_results, start=1):
            st.write(f"{rank}. {name} — {score}%")