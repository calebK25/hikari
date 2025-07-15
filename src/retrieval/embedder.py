from prefect import task, flow
from sentence_transformers import SentenceTransformer

@task(name="embed-batch")
def embed(texts):
    model = SentenceTransformer("BAAI/bge-base-en")
    return model.encode(texts).tolist()

@flow(name="embed-pdf")
def embed_pdf(jsonl_path: str):
    import json
    texts = []
    with open(jsonl_path) as f:
        for line in f:
            texts.append(json.loads(line)["text"])
    vectors = embed(texts)
    # TODO: push to Qdrant


