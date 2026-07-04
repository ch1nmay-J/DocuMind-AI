import time
from src.logger import logger
from src.rag_pipeline import build_pipeline
from src.embeddings import create_query_embedding
from src.retriever import retrieve
from src.llm import generate_answer
from src.utils import similarity_score, relevance_label

# Build the RAG pipeline
chunks, vector_store = build_pipeline()

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
    print("\nSources:\n")

    for rank, (i, distance) in enumerate(
        zip(results, distances),
        start=1
    ):

        print(f"Result {rank}")
        print(f"File  : {chunks[i]['file']}")
        print(f"Page  : {chunks[i]['page']}")
        print(f"Chunk : {chunks[i]['chunk_id']}")

        score = similarity_score(distance)
        label = relevance_label(score)
        print(f"Relevance : {score:.1f}% ({label})")

        print("-" * 40)
    print(f"\nResponse Time: {end-start:.2f} seconds")