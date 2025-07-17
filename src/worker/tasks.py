from .celery_app import celery_app
from src.ingest.ocr import ocr_pdf
from src.retrieval.chunker import split
from src.retrieval.embedder import embed
from qdrant_client import QdrantClient
import json
import pathlib

@celery_app.task(bind=True)
def process_document(self, pdf_path: str):
    """Process a PDF document: OCR → chunk → embed → store in Qdrant"""
    try:
        # Update task state
        self.update_state(state="PROGRESS", meta={"current": 0, "total": 4, "status": "Starting OCR"})
        
        # Step 1: OCR
        pages = ocr_pdf(pdf_path)
        self.update_state(state="PROGRESS", meta={"current": 1, "total": 4, "status": "OCR completed"})
        
        # Step 2: Chunk
        chunks = split(pages)
        self.update_state(state="PROGRESS", meta={"current": 2, "total": 4, "status": "Chunking completed"})
        
        # Step 3: Embed
        vectors = embed([c.page_content for c in chunks])
        self.update_state(state="PROGRESS", meta={"current": 3, "total": 4, "status": "Embedding completed"})
        
        # Step 4: Store in Qdrant
        client = QdrantClient("qdrant", port=6333)
        collection_name = "demo"
        
        # Upload vectors
        client.upload_collection(
            collection_name=collection_name,
            vectors=vectors,
            payload=[
                {"text": c.page_content, "chunk_id": f"doc_{pathlib.Path(pdf_path).stem}_{i:04d}"}
                for i, c in enumerate(chunks)
            ],
        )
        
        self.update_state(state="SUCCESS", meta={"current": 4, "total": 4, "status": "Document processed successfully"})
        return {"status": "success", "chunks_processed": len(chunks)}
        
    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise

@celery_app.task
def answer_question_async(question: str):
    """Answer a question using the RAG system (async version)"""
    from src.retrieval.search import query_search
    
    try:
        answer, citations = query_search(question)
        return {
            "status": "success",
            "answer": answer,
            "citations": citations,
            "question": question
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "question": question
        } 