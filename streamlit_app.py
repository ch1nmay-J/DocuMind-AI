import streamlit as st

from src.pdf_loader import load_uploaded_pdfs
from src.rag_pipeline import build_pipeline
from src.embeddings import create_query_embedding
from src.retriever import retrieve
from src.llm import generate_answer

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📄",
    layout="wide"
)

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

# ==========================
# Sidebar
# ==========================

with st.sidebar:

    st.title("⚙️ Settings")

    st.write(
        """
        Upload one or more PDF files.

        Then ask questions about them.
        """
    )

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.success(f"{len(uploaded_files)} file(s) uploaded!")

        st.subheader("Uploaded Files")

        for file in uploaded_files:

            st.write(f"📄 {file.name}")

# ==========================
# Main Page
# ==========================

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

question = st.text_input(
    "Ask a question about your documents",
    placeholder="Example: What technical skills are mentioned?"
)

ask_button = st.button("🔍 Ask")

# ==========================
# Ask Button
# ==========================

if ask_button:

    if not uploaded_files:

        st.warning("Please upload at least one PDF.")

    elif not question:

        st.warning("Please enter a question.")

    else:

        if not st.session_state.documents_loaded:

            pages = load_uploaded_pdfs(uploaded_files)

            chunks, vector_store = build_pipeline(pages)

            st.session_state.chunks = chunks
            st.session_state.vector_store = vector_store

            st.session_state.documents_loaded = True

            st.success("Documents indexed successfully!")

        chunks = st.session_state.chunks
        vector_store = st.session_state.vector_store
        

        # ----------------------
        # Create Query Embedding
        # ----------------------

        query_embedding = create_query_embedding(question)

        # ----------------------
        # Retrieve Chunks
        # ----------------------

        results, distances = retrieve(
            vector_store,
            query_embedding
        )

        # ----------------------
        # Build Context
        # ----------------------

        context = ""

        for i in results:

            context += f"""
Document: {chunks[i]['file']}
Page: {chunks[i]['page']}

Content:
{chunks[i]['text']}

========================================
"""

        # ----------------------
        # Generate Answer
        # ----------------------

        with st.spinner("🤖 Thinking..."):

            answer = generate_answer(
                question,
                context
            )

        # ----------------------
        # Display Answer
        # ----------------------

        st.subheader("💬 Answer")

        st.info(answer)

        # ----------------------
        # Display Sources
        # ----------------------

        st.subheader("📚 Sources")

        for rank, (index, distance) in enumerate(
            zip(results, distances),
            start=1
        ):

           with st.expander(f"Source {rank}"):

                st.write(f"File : {chunks[index]['file']}")
                st.write(f"Page : {chunks[index]['page']}")
                st.write(f"Chunk : {chunks[index]['chunk_id']}")
                st.write(f"Distance : {distance:.4f}") 

        st.divider()