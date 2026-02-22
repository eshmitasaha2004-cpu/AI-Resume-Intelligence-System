import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

@st.cache_data
def generate_pdf_report(user, score, matched, missing, suggestions):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"User: {user}", styles["Normal"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Match Score: {score}%", styles["Normal"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Matched Skills:", styles["Normal"]))
    elements.append(Paragraph(", ".join(matched), styles["Normal"]))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Missing Skills:", styles["Normal"]))
    elements.append(Paragraph(", ".join(missing), styles["Normal"]))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Suggestions:", styles["Normal"]))
    elements.append(Paragraph(", ".join(suggestions), styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer