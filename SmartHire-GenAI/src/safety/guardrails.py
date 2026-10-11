import re

BLOCKED_PATTERNS = [
    r"\b(?:password|otp|one[- ]time password|credit card|cvv|private key)\b",
    r"\b(?:malware|ransomware|phishing kit|credential theft)\b",
]


def check_llm_input(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("Input is empty.")
    lowered = text.lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, lowered):
            raise ValueError("Input was rejected by SmartHire safety guardrails.")


def is_career_question(question: str) -> bool:
    q = question.lower()
    terms = [
        "career", "job", "resume", "cv", "skill", "interview",
        "role", "employment", "developer", "data", "software",
        "experience", "education", "salary"
    ]
    return any(term in q for term in terms)
