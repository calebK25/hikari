from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from src.llm.openai_llm import chat  # or openrouter_llm.py

client = QdrantClient("qdrant", port=6333)
embedder = SentenceTransformer("BAAI/bge-base-en")

def query_search(q: str):
    """Real retrieval + LLM answer"""
    query_vec = embedder.encode(q).tolist()
    hits = client.search(
        collection_name="demo",
        query_vector=query_vec,
        limit=5
    )
    context = " ".join([h.payload["text"] for h in hits])
    citations = [h.payload["chunk_id"] for h in hits]

    # Ask the LLM
    messages = [
        {"role": "system", "content": "Answer from CONTEXT only."},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQ: {q}"}
    ]
    resp = chat(messages)
    answer = resp.choices[0].message.content

    return answer, citations