import streamlit as st
from datetime import datetime
import pandas as pd
import os
import time

from auth import create_user, login_user
from database import init_db, insert_history, get_user_history, get_leaderboard
from matcher import calculate_match_score
from recruiter import rank_resumes
from resume_parser import extract_text_from_pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def display_tags(title, skills, color):
    st.write(f"### {title}")
    cols = st.columns(4)
    for i, skill in enumerate(skills):
        cols[i % 4].markdown(
            f"<span style='background-color:{color};padding:6px;border-radius:12px;color:white;font-size:12px'>{skill}</span>",
            unsafe_allow_html=True
        )
        def rewrite_suggestions(missing):
         suggestions = []
    for skill in missing[:5]:
        suggestions.append(
            f"Add measurable achievement using '{skill}' (e.g., 'Implemented {skill} improving performance by 20%')."
        )
    return suggestions
def generate_pdf_report(user, score, matched, missing, suggestions):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>AI Resume Intelligence Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"User: {user}", styles["Normal"]))
    elements.append(Paragraph(f"Match Score: {score}%", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Matched Skills:</b>", styles["Heading2"]))
    elements.append(Paragraph(", ".join(matched) if matched else "None", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Missing Skills:</b>", styles["Heading2"]))
    elements.append(Paragraph(", ".join(missing) if missing else "None", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Improvement Suggestions:</b>", styles["Heading2"]))
    elements.append(Paragraph(", ".join(suggestions) if suggestions else "None", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer

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

page = st.sidebar.radio("Navigation", ["Dashboard", "Analyze Resume", "History", "Leaderboard", "Recruiter"])

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
    col1.metric("Total Analysis", total)
    col2.metric("Average Score", f"{avg}%")
    col3.metric("Best Score", f"{best}%")

# ---------------- ANALYZE ----------------

if page == "Analyze Resume":

    st.title("📄 Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    resume_text_input = st.text_area("Or Paste Resume Text")
    job_description = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):

    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_file) if uploaded_file else resume_text_input

    if resume_text and job_description:

        # 1️⃣ Calculate score
        score, matched, missing = calculate_match_score(resume_text, job_description)

        # 2️⃣ Insert into history
        insert_history(st.session_state.user, score, datetime.now())

        # 3️⃣ Metrics
        col1, col2 = st.columns([1, 1])

        with col1:
            st.metric("🎯 Match Score", f"{score}%")

        with col2:
            st.progress(score / 100)

        # 4️⃣ Score Interpretation
        if score < 40:
            st.error("🔴 Low Match – Significant improvement needed.")
        elif score < 70:
            st.warning("🟡 Moderate Match – Some skills missing.")
        else:
            st.success("🟢 Strong Match – Well aligned with job description.")

        # 5️⃣ Skill Analysis
        st.subheader("Skill Analysis")

        st.write("### ✅ Matched Skills")
        if matched:
            st.success(", ".join(matched))
        else:
            st.warning("No strong matches found.")

        st.write("### ❌ Missing Skills")
        if missing:
            st.error(", ".join(missing))
        else:
            st.success("No major skill gaps detected.")

        # 6️⃣ Suggestions
        st.write("### 💡 Improvement Suggestions")
        suggestions = []

        if missing:
            suggestions = [
                f"Consider adding experience related to '{skill}'."
                for skill in missing
            ]

        if suggestions:
            for s in suggestions:
                st.info(s)
        else:
            st.success("Your resume aligns well. Focus on measurable achievements.")

        # 7️⃣ Generate PDF
        pdf_buffer = generate_pdf_report(
            st.session_state.user,
            score,
            matched,
            missing,
            suggestions
        )

        # 8️⃣ Download button
        st.download_button(
            label="📄 Download Analysis Report",
            data=pdf_buffer,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf"
        )

    else:
        st.error("Please upload resume and paste job description.")


             
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
df["Rank"] = range(1, len(df)+1)
df.loc[df["Rank"] == 1, "Rank"] = "🥇 1"
df.loc[df["Rank"] == 2, "Rank"] = "🥈 2"
df.loc[df["Rank"] == 3, "Rank"] = "🥉 3"
df = df[["Rank", "User", "Best Score"]]   
# Highlight logged-in user
current_user = st.session_state.user

user_row = df[df["User"] == current_user]
if not user_row.empty:
    user_rank = user_row.iloc[0]["Rank"]
    st.success(f"🌟 Your Global Rank: {user_rank}")

    def highlight_user(row):
        if row["User"] == current_user:
            return ["background-color: #d4edda"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df.style.apply(highlight_user, axis=1),
        use_container_width=True
    )
else:
    st.dataframe(df, use_container_width=True)


# 📊 Insert Chart HERE
st.subheader("📊 Leaderboard Performance Chart")

chart_df = df.copy()
chart_df["Best Score"] = chart_df["Best Score"].astype(float)

st.bar_chart(
    chart_df.set_index("User")["Best Score"]
)

st.markdown("""
<hr>
<p style='text-align:center; color:#94a3b8;'>
Developed by <b>Eshmita Saha</b><br>
AI Resume Intelligence © 2026
</p>
""", unsafe_allow_html=True)

if page == "Recruiter":

    st.title("📊 Recruiter Dashboard")

    job_description = st.text_area("Paste Job Description")

    uploaded_files = st.file_uploader("Upload Multiple Resumes", accept_multiple_files=True)

    if st.button("Rank Candidates") and job_description and uploaded_files:

        resume_texts = {}

        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resume_texts[file.name] = text

        ranked = rank_resumes(resume_texts, job_description)

        st.write("### Ranking")

        for name, score in ranked:
            st.write(f"{name} — {score}%")

