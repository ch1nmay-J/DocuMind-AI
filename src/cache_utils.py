import os
import pickle
def save_chunks(chunks, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as file:

        pickle.dump(chunks, file)

def load_chunks(filename):

    with open(filename, "rb") as file:

        chunks = pickle.load(file)

    return chunks

def cache_exists(filename):
    return os.path.exists(filename)