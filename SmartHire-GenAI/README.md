# SmartHire GenAI — Resume Matching & AI Career Mentor

A Streamlit-based resume intelligence and career mentoring system following the project specification:
- PDF/DOCX resume parsing
- LLM structured profile extraction
- Semantic job search using local sentence-transformer embeddings + FAISS
- AI CV improvement suggestions
- AI Career Mentor using RAG over jobs and career notes
- Guardrails before LLM calls
- Evaluation utilities
- Streamlit portal

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your Gemini API key.

## Run

```powershell
streamlit run app/streamlit_app.py
```

## Job dataset

Place a Kaggle/pre-collected job CSV in `data/jobs/jobs.csv`. The included demo CSV lets the application run immediately. For the final academic version, replace it with the Kaggle job corpus specified by your project document.

The loader accepts common column names such as:
- title / job_title
- company / company_name
- location / job_location / city
- description / job_description / job_summary / job_desc

## Architecture

Resume -> loader -> Gemini structured parser -> profile
Profile -> local embeddings -> FAISS -> top-N jobs
Resume + jobs -> Gemini CV suggestions
Jobs + career notes -> local embeddings/FAISS -> RAG context -> Gemini mentor
All Gemini calls -> guardrails -> Gemini

## Important

The project intentionally uses local embeddings so semantic-search indexing does not consume Gemini API requests. Gemini is used for generation tasks.
