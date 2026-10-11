import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import json
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.job_search import load_jobs, search_jobs
from src.generate.cv_suggestions import generate_cv_suggestions
from src.mentor.rag_chain import answer_mentor


st.set_page_config(
    page_title="SmartHire GenAI",
    page_icon="💼",
    layout="wide",
)

st.title("💼 SmartHire GenAI")
st.caption("Resume Matching & AI Career Mentor")

st.sidebar.header("SmartHire")
st.sidebar.write("Resume parsing • Semantic job search • CV improvement • RAG mentor")

uploaded = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"],
)

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "profile" not in st.session_state:
    st.session_state.profile = None
if "jobs" not in st.session_state:
    st.session_state.jobs = None
if "matches" not in st.session_state:
    st.session_state.matches = None

if uploaded:
    suffix = Path(uploaded.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        temp_path = tmp.name

    if st.button("🚀 Analyze Resume", type="primary"):
        try:
            with st.spinner("Extracting resume text..."):
                resume_text = load_resume(temp_path)
            st.session_state.resume_text = resume_text

            with st.spinner("Building structured candidate profile with Gemini..."):
                profile = parse_resume(resume_text)
            st.session_state.profile = profile

            with st.spinner("Finding semantically matching jobs..."):
                matches = search_jobs(profile, top_k=5)
            st.session_state.matches = matches
            st.session_state.jobs = load_jobs()

            st.success("Resume analysis completed.")
        except Exception as exc:
            st.error(str(exc))

if st.session_state.profile:
    profile = st.session_state.profile

    st.header("1. Structured Resume Profile")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Name:**", profile.get("name", ""))
        st.write("**Target role:**", profile.get("target_role", ""))
        st.write("**Skills:**")
        st.write(", ".join(profile.get("skills", [])))
    with c2:
        st.write("**Education:**")
        for item in profile.get("education", []):
            st.write("•", item)
        st.write("**Experience:**")
        for item in profile.get("experience", []):
            st.write("•", item)

    st.header("2. Semantic Job Matches")
    matches = st.session_state.matches or []
    if matches:
        table = pd.DataFrame(matches)
        display_cols = [c for c in ["title", "company", "location", "score"] if c in table.columns]
        st.dataframe(table[display_cols], use_container_width=True)
        for i, job in enumerate(matches, 1):
            with st.expander(f"{i}. {job.get('title','')} — {job.get('company','')}"):
                st.write(f"**Location:** {job.get('location','')}")
                st.write(f"**Similarity score:** {job.get('score',0):.3f}")
                st.write(job.get("description", ""))
    else:
        st.info("No job matches available.")

    st.header("3. AI CV Improvement Generator")
    if st.button("Generate CV Improvement Suggestions"):
        try:
            with st.spinner("Generating suggestions..."):
                result = generate_cv_suggestions(
                    st.session_state.resume_text,
                    st.session_state.profile,
                    st.session_state.matches or [],
                )
            st.markdown(result)
        except Exception as exc:
            st.error(str(exc))

    st.header("4. AI Career Mentor")
    if "chat" not in st.session_state:
        st.session_state.chat = []

    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a career question...")
    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        try:
            with st.chat_message("assistant"):
                with st.spinner("Retrieving career context..."):
                    answer = answer_mentor(question, st.session_state.jobs)
                st.markdown(answer)
            st.session_state.chat.append({"role": "assistant", "content": answer})
        except Exception as exc:
            st.error(str(exc))
else:
    st.info("Upload a PDF or DOCX resume and click Analyze Resume.")
