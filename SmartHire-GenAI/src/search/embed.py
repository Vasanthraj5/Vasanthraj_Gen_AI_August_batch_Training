from pathlib import Path
import pickle

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

from src.config import EMBEDDING_MODEL, VECTORSTORE_DIR


_model = None


def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_embedding_model()
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return np.asarray(vectors, dtype="float32")


def save_faiss(index, metadata, name="jobs"):
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(VECTORSTORE_DIR / f"{name}.faiss"))
    with open(VECTORSTORE_DIR / f"{name}_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)


def load_faiss(name="jobs"):
    index_path = VECTORSTORE_DIR / f"{name}.faiss"
    metadata_path = VECTORSTORE_DIR / f"{name}_metadata.pkl"
    if not index_path.exists() or not metadata_path.exists():
        return None, None
    index = faiss.read_index(str(index_path))
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata
