import faiss
import numpy as np
import pickle
import re
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

corpus_chunks = []
sources = []
index = None

def split_text_into_chunks(text, chunk_size=500, overlap=50):
    text = re.sub(r'\s+', ' ', text).strip()
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def embed_and_store(text, title):
    global corpus_chunks, sources, index

    chunks = split_text_into_chunks(text)
    vectors = embed_model.encode(chunks)

    if index is None:
        index = faiss.IndexFlatL2(vectors.shape[1])

    # Avoid duplicate chunks
    index.add(np.array(vectors))
    corpus_chunks.extend(chunks)
    sources.extend([title] * len(chunks))

    save_vector_store()
    print(f"[RAG] Stored {len(chunks)} chunks from {title}")


def load_vector_store():
    global corpus_chunks, sources, index
    try:
        with open("vector_store.pkl", "rb") as f:
            data = pickle.load(f)
            corpus_chunks = data["chunks"]
            sources = data["sources"]
            index = data["index"]
            print(f"[RAG] Loaded vector store with {len(corpus_chunks)} chunks")
    except FileNotFoundError:
        print("[RAG] No vector store found. Please upload documents.")
        corpus_chunks, sources, index = [], [], None

    return corpus_chunks, sources, index, embed_model

def load_vector_db():
    return corpus_chunks, sources, index, embed_model

import pickle

def save_vector_store():
    global corpus_chunks, sources, index
    with open("vector_store.pkl", "wb") as f:
        pickle.dump({
            "chunks": corpus_chunks,
            "sources": sources,
            "index": index
        }, f)
    print(f"[RAG] Saved vector store with {len(corpus_chunks)} chunks.")


