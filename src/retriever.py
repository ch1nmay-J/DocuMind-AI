import numpy as np

def retrieve(index, query_embedding, k=3):
    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, k)
    
    return indices[0]