#!/usr/bin/env python3
"""
One-shot script:
  1. Reads sample_data/scan.jsonl  (pages from OCR)
  2. Chunks → embeds → uploads to Qdrant collection 'demo'
"""

import json, sys, pathlib
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------- config ----------------
COLLECTION = "demo"
JSONL_PATH = pathlib.Path("sample_data/scan.jsonl")
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
# ---------------------------------------

client = QdrantClient("qdrant", port=6333)
embedder = SentenceTransformer("BAAI/bge-base-en")

# 1. Load text
if not JSONL_PATH.exists():
    sys.exit(f"{JSONL_PATH} not found. Run OCR first.")
pages = [json.loads(l)["text"] for l in JSONL_PATH.open()]

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)
chunks = splitter.create_documents(["\n".join(pages)])

# 3. Embed
vectors = embedder.encode([c.page_content for c in chunks]).tolist()

# 4. Create / recreate collection
if client.collection_exists(COLLECTION):
    client.delete_collection(COLLECTION)
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=models.VectorParams(size=len(vectors[0]), distance=models.Distance.COSINE)
)

# 5. Upload
client.upload_collection(
    collection_name=COLLECTION,
    vectors=vectors,
    payload=[
        {"text": c.page_content, "chunk_id": f"c{i:04d}"}
        for i, c in enumerate(chunks)
    ],
)
# 
payload = [
    {
        "text": c.page_content,
        "chunk_id": f"c{i:04d}",
        "page": 1  # quick stub; later use layout-parser bbox
    }
    for i, c in enumerate(chunks)
]
print(f"Seeded {len(chunks)} chunks into '{COLLECTION}'")