import streamlit as st
import pandas as pd
from datetime import datetime

from database import init_db, insert_history, get_user_history, get_leaderboard
from utils import extract_text_from_pdf
from score import calculate_match_score

# Initialize database
init_db()

# -----------------------
# Navigation
# -----------------------

page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Analyze Resume", "Leaderboard"]
)

# -----------------------
# DASHBOARD
# -----------------------

if page == "Dashboard":

    st.title("📊 Dashboard")

    user = st.session_state.get("user", "Guest")
    history = get_user_history(user)

    total = len(history)
    avg_score = sum([row[1] for row in history]) / total if total else 0
    best_score = max([row[1] for row in history]) if total else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Analysis", total)
    col2.metric("Average Score", f"{avg_score:.1f}%")
    col3.metric("Best Score", f"{best_score}%")

# -----------------------
# ANALYZE RESUME
# -----------------------

elif page == "Analyze Resume":

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
                resume_text,
                job_description
            )

            insert_history(
                st.session_state.get("user", "Guest"),
                score,
                datetime.now()
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🎯 Match Score", f"{score}%")

            with col2:
                st.progress(score / 100)

            # Score Interpretation
            if score < 40:
                st.error("🔴 Low Match — Significant improvement needed.")
            elif score < 70:
                st.warning("🟡 Moderate Match — Some skills missing.")
            else:
                st.success("🟢 Strong Match — Well aligned with job description.")

            # Skills
            st.subheader("Skill Analysis")

            if matched:
                st.success("Matched Skills: " + ", ".join(matched))
            else:
                st.warning("No strong matches found.")

            if missing:
                st.error("Missing Skills: " + ", ".join(missing))
            else:
                st.success("No major skill gaps detected.")

        else:
            st.error("Please upload resume and paste job description.")

# -----------------------
# LEADERBOARD
# -----------------------

elif page == "Leaderboard":

    st.title("🏆 Leaderboard")

    history = get_leaderboard()

    if history:
        df = pd.DataFrame(history, columns=["User", "Score"])
        df = df.sort_values(by="Score", ascending=False)
        df["Rank"] = range(1, len(df) + 1)

        st.dataframe(df)

        current_user = st.session_state.get("user")

        if current_user:
            user_row = df[df["User"] == current_user]

            if not user_row.empty:
                st.success(
                    f"Your Rank: {int(user_row['Rank'].values[0])}"
                )
    else:
        st.info("No leaderboard data yet.")