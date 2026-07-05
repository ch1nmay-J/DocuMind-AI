import os
import pickle
def save_chunks(chunks, filename):

    with open(filename, "wb") as file:

        pickle.dump(chunks, file)

def load_chunks(filename):

    with open(filename, "rb") as file:

        chunks = pickle.load(file)

    return chunks

def cache_exists(filename):
    return os.path.exists(filename)