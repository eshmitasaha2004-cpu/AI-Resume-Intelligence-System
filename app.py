import streamlit as st
import pandas as pd
from datetime import datetime

from utils import extract_text_from_pdf
from score import calculate_match_score
from database import init_db, insert_history, get_all_history

# Initialize database
init_db()

# ---------------------------
# LOGIN SYSTEM
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title(f"Welcome, {st.session_state.user}")
page = st.sidebar.selectbox(
    "Navigation",
    ["Analyze Resume", "Dashboard", "Leaderboard"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# ---------------------------
# ANALYZE RESUME PAGE
# ---------------------------
if page == "Analyze Resume":

    st.title("📄 Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    resume_text_input = st.text_area("Or Paste Resume Text")
    job_description = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):

        resume_text = (
            extract_text_from_pdf(uploaded_file)
            if uploaded_file
            else resume_text_input
        )

        if resume_text and job_description:

            score, matched, missing = calculate_match_score(
                resume_text, job_description
            )

            st.metric("Match Score", f"{score}%")
            st.progress(score / 100)

            st.subheader("Matched Skills")
            st.write(", ".join(matched) if matched else "None")

            st.subheader("Missing Skills")
            st.write(", ".join(missing) if missing else "None")

            # Save to database
            insert_history(
                st.session_state.user,
                score,
                datetime.now()
            )

        else:
            st.error("Please upload resume and paste job description.")

# ---------------------------
# DASHBOARD PAGE
# ---------------------------
elif page == "Dashboard":

    st.title("📊 Dashboard")

    df = get_all_history()

    if not df.empty:

        user_df = df[df["user"] == st.session_state.user]

        total = len(user_df)
        avg_score = int(user_df["score"].mean())
        best_score = int(user_df["score"].max())

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Analysis", total)
        col2.metric("Average Score", f"{avg_score}%")
        col3.metric("Best Score", f"{best_score}%")

    else:
        st.info("No analysis data yet.")

# ---------------------------
# LEADERBOARD PAGE
# ---------------------------
elif page == "Leaderboard":

    st.title("🏆 Leaderboard")

    df = get_all_history()

    if not df.empty:

        leaderboard = (
            df.groupby("user")["score"]
            .max()
            .reset_index()
            .sort_values(by="score", ascending=False)
        )

        st.dataframe(leaderboard)

    else:
        st.info("No leaderboard data yet.")