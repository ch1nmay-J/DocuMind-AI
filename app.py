import time
from src.logger import logger
from src.rag_pipeline import build_pipeline
from src.embeddings import create_query_embedding
from src.retriever import retrieve
from src.llm import generate_answer
from src.utils import similarity_score, relevance_label
from src.source_formatter import format_sources
from src.pdf_loader import load_all_pdfs

# Build the RAG pipeline
pages = load_all_pdfs("data")
chunks, vector_store = build_pipeline(pages)

while True:

    query = input("\nAsk a question (type 'exit' to quit): ")
    logger.info(f"User Question: {query}")

    if query.lower() == "exit":
        print("\nGoodbye!")
        break

    # Create embedding for the question
    query_embedding = create_query_embedding(query)

    logger.info("Retrieving relevant chunks...")
    # Retrieve relevant chunks
    results, distances = retrieve(vector_store, query_embedding)

    # Build context
    context = ""

    for i in results:

        context += f"""
Document: {chunks[i]['file']}
Page: {chunks[i]['page']}

Content:
{chunks[i]['text']}

========================================
"""

    logger.info("Generating response using Gemini...")

    start = time.time()

    # Generate answer
    answer = generate_answer(query, context)

    end = time.time()

    logger.info("Response generated succesfully.")

    # Display answer
    print("\nAnswer:\n")
    print(answer)

    # Display sources
format_sources(results, distances, chunks)

print(f"\nResponse Time: {end-start:.2f} seconds")