from src.config import TOP_K_RESULTS
import numpy as np

def retrieve(index, query_embedding, k=TOP_K_RESULTS):
    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, k)
    
    return indices[0], distances[0]