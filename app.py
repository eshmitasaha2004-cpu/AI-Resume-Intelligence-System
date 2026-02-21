import streamlit as st
from datetime import datetime
import pandas as pd
import os
import time

from auth import create_user, login_user
from database import init_db, insert_history, get_user_history, get_leaderboard
from matcher import calculate_match_score
from resume_parser import extract_text_from_pdf

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="🚀",
    layout="wide"
)

init_db()



if "user" not in st.session_state:
    st.session_state.user = None

    if "login_error" not in st.session_state:
    st.session_state.login_error = False

# ---------------- AUTH ----------------
if not st.session_state.user:

    mode = st.radio("Select Mode", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Sign Up":
        if st.button("Create Account"):
            if create_user(email, password):
                st.success("Account created successfully!")
            else:
                st.error("User already exists!")

    if mode == "Login":
        if st.button("Login"):
            if login_user(email, password):
                st.session_state.user = email
                st.rerun()
            else:
                st.error("Invalid credentials!")

    st.stop()


    type_writer("AI Resume Enhancement")

    

    mode = st.sidebar.radio("Select Mode", ["Login", "Sign Up"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if mode == "Sign Up":
        if st.sidebar.button("Create Account"):
            if create_user(email, password):
                st.success("Account created successfully!")
            else:
                st.error("User already exists!")

    if mode == "Login":
      login_clicked = st.button("Login")

      if login_clicked:
         if login_user(email, password):
            st.session_state.user = email
            st.session_state.login_error = False
            st.rerun()
         else:
            st.session_state.login_error = True

    if st.session_state.get("login_error"):
        st.error("Invalid credentials!")

    st.stop()

# ---------------- MAIN NAV ----------------

st.sidebar.success(f"Logged in as {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

page = st.sidebar.radio("Navigation", ["Dashboard", "Analyze Resume", "History", "Leaderboard"])

# ---------------- DASHBOARD ----------------

if page == "Dashboard":
    score = 0
    st.title("📊 Dashboard")

    history = get_user_history(st.session_state.user)

    scores = [row[0] for row in history]

    total = len(scores)
    avg = round(sum(scores)/len(scores), 2) if scores else 0
    best = max(scores) if scores else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Analyses", total)
    col2.metric("Average Score", f"{avg}%")
    col3.metric("Best Score", f"{best}%")

# ---------------- ANALYZE ----------------

if page == "Analyze Resume":

    st.title("📄 Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    resume_text_input = st.text_area("Or Paste Resume Text")
    job_description = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):

        resume_text = extract_text_from_pdf(uploaded_file) if uploaded_file else resume_text_input

        if resume_text and job_description:

            score = calculate_match_score(resume_text, job_description)
            insert_history(st.session_state.user, score, datetime.now())

            col1, col2 = st.columns([1,1])
 
            with col1:
             st.metric("🎯 Match Score", f"{score}%")

            with col2:
             st.progress(score / 100)
    else:
     st.error("please upload resume and paste job description")

 

st.markdown("---")


# ---------------- HISTORY ----------------

if page == "History":

    st.title("📈 History")

    history = get_user_history(st.session_state.user)

    if history:
        df = pd.DataFrame(history, columns=["Match Score", "Timestamp"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No history found.")

# ---------------- LEADERBOARD ----------------
if page == "Leaderboard":
    st.title("🏆 Global Leaderboard")

    leaderboard = get_leaderboard()

    if leaderboard:
        df = pd.DataFrame(leaderboard, columns=["User", "Best Score"])
        df = df.sort_values("Best Score", ascending=False)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No leaderboard data yet.")
   

else:
            st.error("Invalid credentials!")

st.markdown('</div>', unsafe_allow_html=True)
st.stop()

st.markdown("""
<hr>
<p style='text-align:center; color:#94a3b8;'>
Developed by <b>Eshmita Saha</b><br>
AI Resume Intelligence © 2026
</p>
""", unsafe_allow_html=True)

