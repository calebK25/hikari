#!/usr/bin/env python3
"""
Runs all questions once → DuckDB table metrics
"""
import json, time, duckdb, requests

with open("src/eval/questions.json") as f:
    qs = json.load(f)

conn = duckdb.connect("eval.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS metrics (
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    q TEXT,
    latency DOUBLE,
    answer TEXT,
    expected TEXT
)
""")

rows = []
for qa in qs:
    t0 = time.time()
    resp = requests.post("http://localhost:8000/query",
                         json={"q": qa["q"]}).json()
    latency = time.time() - t0
    rows.append((qa["q"], latency, resp["answer"], qa["a"]))

conn.executemany(
    "INSERT INTO metrics (q, latency, answer, expected) VALUES (?,?,?,?)",
    rows
)
print("Eval done –", len(rows), "rows inserted")