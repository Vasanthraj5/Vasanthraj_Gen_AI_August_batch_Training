from pathlib import Path
import json


def evaluate_retrieval(results, expected_keywords):
    text = " ".join(
        f"{r.get('title','')} {r.get('description','')}"
        for r in results
    ).lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in text)
    return {
        "keyword_hit_count": hits,
        "keyword_count": len(expected_keywords),
        "hit_rate": hits / len(expected_keywords) if expected_keywords else 0.0,
    }


def save_evaluation(result: dict, path=None):
    path = Path(path or "reports/evaluation.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
