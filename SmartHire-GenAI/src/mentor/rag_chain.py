from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CAREER_NOTES_DIR, client, GEMINI_MODEL
from src.generate.prompts import mentor_prompt
from src.safety.guardrails import check_llm_input, is_career_question
from src.search.embed import embed_texts


def load_career_documents(jobs):
    docs = []

    for _, row in jobs.iterrows():
        text = (
            f"Job title: {row.get('title','')}\n"
            f"Company: {row.get('company','')}\n"
            f"Location: {row.get('location','')}\n"
            f"Description: {row.get('description','')}"
        )
        docs.append(Document(page_content=text, metadata={"type": "job"}))

    if CAREER_NOTES_DIR.exists():
        for path in CAREER_NOTES_DIR.glob("*.txt"):
            docs.append(
                Document(
                    page_content=path.read_text(encoding="utf-8"),
                    metadata={"type": "career_note", "source": path.name},
                )
            )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
    )
    return splitter.split_documents(docs)


def retrieve_context(question: str, documents, top_k=5):
    if not documents:
        return ""

    texts = [d.page_content for d in documents]
    vectors = embed_texts(texts)
    q = embed_texts([question])

    scores = (vectors @ q[0]).tolist()
    ranked = sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True,
    )[:top_k]

    return "\n\n---\n\n".join(
        f"[Source {i+1}]\n{doc.page_content}"
        for i, (_, doc) in enumerate(ranked)
    )


def answer_mentor(question: str, jobs):
    check_llm_input(question)

    if not is_career_question(question):
        return "Please ask a question related to careers, resumes, skills, jobs, interviews, or professional development."

    documents = load_career_documents(jobs)
    context = retrieve_context(question, documents)

    if not context:
        return "I don't have enough retrieved career information to answer that."

    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=mentor_prompt(question, context),
    )
    return response.output_text.strip()
