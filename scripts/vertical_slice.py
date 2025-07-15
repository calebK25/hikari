from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from openai import OpenAI

pdf_path = "sample_data/math_paper.pdf"
q = "What is the main topic and key findings of this mathematical paper?"

loader = PyPDFLoader(pdf_path)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embedder = SentenceTransformer("BAAI/bge-base-en")
vectors = embedder.encode([c.page_content for c in chunks]).tolist()

client = QdrantClient(":memory:")
client.create_collection(
    collection_name="demo",
    vectors_config=models.VectorParams(size=len(vectors[0]), distance=models.Distance.COSINE)
)
client.upload_collection("demo", vectors=vectors, payload=[{"text": c.page_content} for c in chunks])

hits = client.query_points("demo", query=embedder.encode(q).tolist(), limit=5)
context = " ".join([h.payload["text"] for h in hits.points])

# Use OpenRouter with Kimi Dev 72B model
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="OPENROUTER_API_KEY"
)

resp = client.chat.completions.create(
    model="moonshotai/kimi-dev-72b:free",
    messages=[
        {"role": "system", "content": "Answer from CONTEXT only."},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQ: {q}"}
    ],
    temperature=0.7,
    max_tokens=512
)

print("Answer:", resp.choices[0].message.content)