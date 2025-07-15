import json, time, duckdb, requests
with open("eval/questions.json") as f:
    qs = json.load(f)
rows = []
for qa in qs:
    t0 = time.time()
    r = requests.post("http://localhost:8000/query", json={"q": qa["q"]}).json()
    rows.append({"q": qa["q"], "latency": time.time()-t0, "answer": r["answer"]})
duckdb.connect("eval.db").execute("CREATE OR REPLACE TABLE metrics AS SELECT * FROM rows")