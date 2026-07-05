import streamlit as st

from src.pdf_loader import load_uploaded_pdfs
from src.rag_pipeline import build_pipeline
from src.embeddings import create_query_embedding
from src.retriever import retrieve
from src.llm import generate_answer

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "document_names" not in st.session_state:
    st.session_state.document_names = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

    st.divider()

    clear_chat = st.button("🗑️ Clear Chat")

    if clear_chat:

        st.session_state.chat_history = []

        st.success("Chat history cleared!")

    st.divider()

    with st.expander("ℹ️ About"):

        st.write(
            """
    This application uses Retrieval-Augmented Generation (RAG)
    to answer questions from uploaded PDF documents.

    Pipeline:

    PDF → Chunks → Embeddings → FAISS → Gemini
    """
        )
    
    with st.expander("🛠 Tech Stack"):

        st.markdown("""
    - Python
    - Streamlit
    - LangChain
    - FAISS
    - Sentence Transformers
    - Gemini API
    - PyMuPDF
    """)

# ==========================
# Main Page
# ==========================

st.title("📄 DocuMind AI")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Documents Uploaded",
        len(uploaded_files) if uploaded_files else 0
    )

with col2:
    st.metric(
        "Questions Asked",
        len(st.session_state.chat_history)
    )

st.caption(
    "Upload PDF documents and ask natural language questions using Retrieval-Augmented Generation (RAG)."
)

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

        current_documents = sorted(
            [file.name for file in uploaded_files]
        )

        if (
            not st.session_state.documents_loaded
            or
            current_documents != st.session_state.document_names
        ):

            pages = load_uploaded_pdfs(uploaded_files)

            chunks, vector_store = build_pipeline(pages)

            st.session_state.chunks = chunks
            st.session_state.vector_store = vector_store

            st.session_state.documents_loaded = True

            st.session_state.document_names = current_documents

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
        
        st.session_state.chat_history.append(
            (question, answer)
        )

        # ----------------------
        # Display Answer
        # ----------------------

        with st.container():

            st.subheader("💬 Answer")

            st.info(answer)

        # ----------------------
        # Display Sources
        # ----------------------
        with st.container():
        
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

st.divider()

st.subheader("💬 Chat History")

if not st.session_state.chat_history:

    st.info("No conversation yet. Ask your first question!")

else:

    for q, a in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(q)

        with st.chat_message("assistant"):
            st.write(a)

st.divider()

st.caption(
    "Built with ❤️ using Streamlit, LangChain, FAISS, Sentence Transformers and Gemini."
)