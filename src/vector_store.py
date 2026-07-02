import faiss
import numpy as np
def create_vector_store(embeddings):
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)
    
    return index