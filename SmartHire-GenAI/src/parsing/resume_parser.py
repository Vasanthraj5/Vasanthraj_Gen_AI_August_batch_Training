import json
from src.config import client, GEMINI_MODEL
from src.safety.guardrails import check_llm_input

RESUME_SCHEMA = {
    "name": "",
    "skills": [],
    "experience": [],
    "education": [],
    "target_role": "",
}


def build_resume_prompt(resume_text: str) -> str:
    return f'''
You are a resume information extraction system.

Analyze the resume text below and extract the candidate's information.

Return ONLY valid JSON. Do not add markdown or explanations.
Do not invent information that is not present.

Use exactly this structure:
{json.dumps(RESUME_SCHEMA, indent=2)}

Rules:
- name: candidate's full name.
- skills: technical and professional skills explicitly mentioned.
- experience: work, internship and relevant project experience.
- education: educational qualifications.
- target_role: stated objective/target role, or the clearest target role.
- Missing information must be an empty string or empty list.
- Preserve facts from the resume.

RESUME TEXT:
{resume_text}
'''


def _clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    return text


def validate_resume_profile(profile: dict) -> None:
    if not isinstance(profile, dict):
        raise ValueError("Resume profile must be a JSON object.")
    for field in ["name", "skills", "experience", "education", "target_role"]:
        if field not in profile:
            raise ValueError(f"Missing required resume field: {field}")
    if not isinstance(profile["name"], str):
        raise ValueError("'name' must be a string.")
    if not isinstance(profile["skills"], list):
        raise ValueError("'skills' must be a list.")
    if not isinstance(profile["experience"], list):
        raise ValueError("'experience' must be a list.")
    if not isinstance(profile["education"], list):
        raise ValueError("'education' must be a list.")
    if not isinstance(profile["target_role"], str):
        raise ValueError("'target_role' must be a string.")


def parse_resume(resume_text: str) -> dict:
    if not resume_text.strip():
        raise ValueError("Resume text is empty.")
    check_llm_input(resume_text)

    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=build_resume_prompt(resume_text),
    )
    response_text = _clean_json(response.output_text)
    try:
        profile = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Gemini returned invalid JSON: {response_text}") from exc
    validate_resume_profile(profile)
    return profile
