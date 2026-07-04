import streamlit as st

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📄",
    layout="wide"
)

st.title("📄 RAG Document Q&A System")

st.write(
    """
Welcome!

This application lets you upload PDF documents
and ask questions about them using Retrieval
Augmented Generation (RAG).
"""
)

st.divider()

st.header("Ask Questions About Your Documents")