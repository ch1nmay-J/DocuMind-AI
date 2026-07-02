from src.pdf_loader import load_pdf
from src.text_splitter import split_text
from src.embeddings import create_embeddings
from src.vector_store import create_vector_store


def build_pipeline(pdf_path):

    pdf = load_pdf(pdf_path)

    all_text = ""

    for page in pdf:
        all_text += page.get_text()

    chunks = split_text(all_text)

    embeddings = create_embeddings(chunks)

    vector_store = create_vector_store(embeddings)

    return chunks, vector_store