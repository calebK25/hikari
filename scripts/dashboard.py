import streamlit as st, duckdb
df = duckdb.connect("eval.db").query("SELECT * FROM metrics").df()
st.title("RAG Metrics")
st.dataframe(df)
st.line_chart(df, x="q", y="latency")