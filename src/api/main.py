from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os, pathlib
from celery.result import AsyncResult
# Optional Celery imports - API will work without Celery
try:
    from src.worker.celery_app import celery_app
    from src.worker.tasks import process_document, answer_question_async
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    print("Warning: Celery not available. Async endpoints will not work.")
from src.retrieval.search import query_search
from prometheus_fastapi_instrumentator import Instrumentator

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

app = FastAPI()

Instrumentator().instrument(app).expose(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    q: str

@app.post("/query")
def query(q: Query):
    answer, cites = query_search(q.q)
    return {"answer": answer, "citations": cites}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not CELERY_AVAILABLE:
        return {"error": "Celery not available. Install with: pip install 'celery[redis]' redis"}
    
    file_path = pathlib.Path("uploads") / file.filename
    pathlib.Path("uploads").mkdir(exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    job = process_document.delay(str(file_path))
    return {"job_id": job.id}

@app.get("/jobs/{job_id}")
def job_status(job_id: str):
    if not CELERY_AVAILABLE:
        return {"error": "Celery not available"}
    
    res = AsyncResult(job_id, app=celery_app)
    return {"status": res.status, "result": res.result}

@app.post("/query-async")
def query_async(q: Query):
    if not CELERY_AVAILABLE:
        return {"error": "Celery not available. Install with: pip install 'celery[redis]' redis"}
    
    job = answer_question_async.delay(q.q)
    return {"job_id": job.id}

