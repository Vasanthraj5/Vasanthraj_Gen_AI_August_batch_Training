import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY was not found. Add it to .env.")

client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-3.8-flash"

DATA_DIR = BASE_DIR / "data"
JOBS_DIR = DATA_DIR / "jobs"
RESUMES_DIR = DATA_DIR / "resumes"
CAREER_NOTES_DIR = DATA_DIR / "career_notes"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
REPORTS_DIR = BASE_DIR / "reports"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5
