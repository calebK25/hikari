from fastapi import FastAPI
from pydantic import BaseModel
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from retrieval.search import query_search
from prometheus_fastapi_instrumentator import Instrumentator



app = FastAPI()
Instrumentator().instrument(app).expose(app)


class Query(BaseModel):
    q: str

@app.post("/query")
def query(q: Query):
    answer, cites = query_search(q.q)
    return {"answer": answer, "citations": cites}