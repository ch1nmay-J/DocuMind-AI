import os
import faiss
import numpy as np
def create_vector_store(embeddings):
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)
    
    return index

def save_vector_store(index, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    faiss.write_index(index, filename)
    

def load_vector_store(filename):
    return faiss.read_index(filename)

def vector_store_exists(filename):
    return os.path.exists(filename)