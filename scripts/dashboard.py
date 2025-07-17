import streamlit as st, duckdb

# Use a context manager to properly handle the connection
with duckdb.connect("eval.db") as conn:
    df = conn.query("SELECT * FROM metrics").df()
st.title("RAG Metrics")
st.dataframe(df)
st.line_chart(df, x="q", y="latency")

# Precision@5 placeholder (manual 1/0 for now)
df["correct"] = (df["answer"].str.lower() == df["expected"].str.lower()).astype(int)
st.metric("P@1 (manual)", f"{df['correct'].mean():.2%}")
st.metric("Avg latency (ms)", f"{(df['latency']*1000).mean():.0f}")
st.line_chart(df, x="q", y="latency")