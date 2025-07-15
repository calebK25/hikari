import duckdb, os
def chat(messages, model="gpt-4o-mini"):
    resp = client.chat.completions.create(model=model, messages=messages)
    usage = resp.usage
    duckdb.connect("eval.db").execute(
        "INSERT INTO usage (ts, model, prompt, completion) VALUES (now(), ?, ?, ?)",
        [model, usage.prompt_tokens, usage.completion_tokens]
    )
    return resp