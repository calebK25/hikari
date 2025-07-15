from prefect import flow, task
from pathlib import Path
import json
from src.ingest.ocr import ocr_pdf
from src.retrieval.chunker import split

@task
def process_pdf(pdf_path: str) -> list:
    """Process a PDF file and return OCR'd pages"""
    pages = ocr_pdf(pdf_path)
    return pages

@task
def chunk_pages(pages: list) -> list:
    """Split pages into chunks for vector storage"""
    chunks = split(pages)
    return chunks

@task
def save_chunks(chunks: list, output_path: str):
    """Save chunks to a file for later processing"""
    with open(output_path, 'w') as f:
        for chunk in chunks:
            f.write(json.dumps({
                "content": chunk.page_content,
                "metadata": chunk.metadata
            }) + "\n")

@flow(name="nightly-document-ingest")
def nightly_ingest_flow():
    """Main flow for nightly document ingestion"""
    
    # Define input and output paths
    sample_dir = Path("sample_data")
    output_dir = Path("processed_data")
    output_dir.mkdir(exist_ok=True)
    
    # Process each PDF in the sample directory
    for pdf_file in sample_dir.glob("*.pdf"):
        print(f"Processing {pdf_file}")
        
        # Step 1: OCR the PDF
        pages = process_pdf(str(pdf_file))
        
        # Step 2: Chunk the pages
        chunks = chunk_pages(pages)
        
        # Step 3: Save chunks
        output_file = output_dir / f"{pdf_file.stem}_chunks.jsonl"
        save_chunks(chunks, str(output_file))
        
        print(f"Completed processing {pdf_file} -> {output_file}")

if __name__ == "__main__":
    nightly_ingest_flow() 