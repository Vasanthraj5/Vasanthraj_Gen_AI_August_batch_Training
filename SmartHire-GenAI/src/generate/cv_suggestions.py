from src.config import client, GEMINI_MODEL
from src.safety.guardrails import check_llm_input
from src.generate.prompts import build_cv_improvement_prompt


def generate_cv_suggestions(resume_text: str, profile: dict, jobs: list) -> str:
    """Generate AI-powered CV improvement suggestions."""

    check_llm_input(resume_text)

    prompt = build_cv_improvement_prompt(
        resume_text=resume_text,
        profile=profile,
        jobs=jobs,
    )

    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
    )

    return response.output_text.strip()