from src.rag_pipeline import build_pipeline
from src.embeddings import create_query_embedding
from src.retriever import retrieve
from src.llm import generate_answer

# Build the RAG pipeline
chunks, vector_store = build_pipeline("data/chinmay_j.pdf")

# Ask the user a question
query = input("Ask a question: ")

# Convert the question into an embedding
query_embedding = create_query_embedding(query)

# Retrieve the most relevant chunks
results = retrieve(vector_store, query_embedding)

# Combine the retrieved chunks into one context
context = ""

for i in results:
    context += chunks[i]
    context += "\n\n"

# Generate the final answer using Gemini
answer = generate_answer(query, context)

# Print the answer
print("\nAnswer:\n")
print(answer)