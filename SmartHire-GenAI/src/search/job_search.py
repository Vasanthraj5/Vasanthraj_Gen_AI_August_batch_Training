from pathlib import Path
import pandas as pd
import faiss

from src.config import JOBS_DIR, TOP_K
from src.search.embed import embed_texts, save_faiss, load_faiss


COLUMN_ALIASES = {
    "title": ["title", "job_title", "Job_title", "TITLE"],
    "company": ["company", "company_name", "Company", "COMPANY_NAME"],
    "location": ["location", "job_location", "city", "State/City", "LOCATION"],
    "description": [
        "description",
        "job_description",
        "job_summary",
        "job_desc",
        "Job_Desc",
        "description_raw",
    ],
}


def _find_column(df, aliases):
    for col in aliases:
        if col in df.columns:
            return col
    return None


def _items_to_text(items) -> str:
    """
    Convert a profile field into searchable text.

    Supports:
    - strings
    - dictionaries
    - lists containing strings/dictionaries
    """
    if not items:
        return ""

    if isinstance(items, str):
        return items

    if isinstance(items, dict):
        return " ".join(
            str(value)
            for value in items.values()
            if value not in (None, "")
        )

    if isinstance(items, list):
        parts = []

        for item in items:
            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):
                parts.append(
                    " ".join(
                        str(value)
                        for value in item.values()
                        if value not in (None, "")
                    )
                )

            else:
                parts.append(str(item))

        return " ".join(parts)

    return str(items)


def load_jobs(csv_path: str | None = None) -> pd.DataFrame:
    path = Path(csv_path) if csv_path else JOBS_DIR / "jobs.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"Job dataset not found: {path}. "
            "Put a CSV in data/jobs/jobs.csv."
        )

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Job dataset is empty.")

    normalized = {}

    for target, aliases in COLUMN_ALIASES.items():
        source = _find_column(df, aliases)

        if source:
            normalized[target] = df[source].fillna("").astype(str)
        else:
            normalized[target] = ""

    out = pd.DataFrame(normalized)

    out["job_id"] = range(len(out))

    out["search_text"] = (
        out["title"]
        + " | "
        + out["company"]
        + " | "
        + out["location"]
        + " | "
        + out["description"]
    ).str.strip()

    return out


def build_job_index(df: pd.DataFrame):
    vectors = embed_texts(df["search_text"].tolist())

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    metadata = df.to_dict(orient="records")

    save_faiss(index, metadata)

    return index, metadata


def get_or_build_index(df: pd.DataFrame):
    index, metadata = load_faiss()

    if (
        index is not None
        and metadata
        and index.ntotal == len(df)
    ):
        return index, metadata

    return build_job_index(df)


def search_jobs(profile: dict, top_k: int = TOP_K):
    df = load_jobs()

    index, metadata = get_or_build_index(df)

    profile_text_parts = [
        _items_to_text(profile.get("name", "")),
        _items_to_text(profile.get("target_role", "")),
        _items_to_text(profile.get("skills", [])),
        _items_to_text(profile.get("experience", [])),
        _items_to_text(profile.get("education", [])),
    ]

    profile_text = " ".join(
        part for part in profile_text_parts if part
    )

    if not profile_text.strip():
        return []

    query = embed_texts([profile_text])

    scores, indices = index.search(
        query,
        min(top_k, index.ntotal),
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        item = dict(metadata[idx])
        item["score"] = float(score)

        results.append(item)

    return results