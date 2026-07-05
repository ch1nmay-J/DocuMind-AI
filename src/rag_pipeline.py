from src.cache import (
    save_chunks,
    load_chunks,
    cache_exists
)
from src.pdf_loader import load_all_pdfs
from src.text_splitter import split_text
from src.embeddings import create_embeddings
from src.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    vector_store_exists
    )


def build_pipeline(pages):

    if cache_exists("chunks.pkl"):

        print("Loading cached chunks...")

        chunks = load_chunks("chunks.pkl")

    else:

        chunks = split_text(pages)

        save_chunks(chunks, "chunks.pkl")


    if vector_store_exists("vector_store.index"):

        print("Loading cached FAISS index...")

        vector_store = load_vector_store("vector_store.index")

    else:

        embeddings = create_embeddings(chunks)

        vector_store = create_vector_store(embeddings)

        save_vector_store(vector_store, "vector_store.index")

    return chunks, vector_store