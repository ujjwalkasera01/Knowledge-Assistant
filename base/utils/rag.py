import os
from dotenv import load_dotenv
import numpy as np
from transformers import pipeline
from .embedding import load_vector_db, load_vector_store, embed_model

# Load HuggingFace model
load_dotenv()
qa_pipeline = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2",
    token=os.getenv("HF_TOKEN")
)


corpus_chunks, sources, index, model = None, None, None, embed_model

def initialize_vector_store():
    global corpus_chunks, sources, index
    corpus_chunks, sources, index, _ = load_vector_db()
    if not corpus_chunks:
        load_vector_store()
        corpus_chunks, sources, index, _ = load_vector_db()


def retrieve_answer(question):
    if not corpus_chunks:
        initialize_vector_store()

    if not corpus_chunks:
        return "Knowledge base is empty. Please upload a document first.", []

    print(f"[RAG] Chunks loaded: {len(corpus_chunks)}")

    D, I = index.search(model.encode([question]), k=5)
    context = "\n".join([corpus_chunks[i] for i in I[0]])

    qa_input = {
    "question": question,
    "context": context,
}

    result = qa_pipeline(qa_input)

    answer = result["answer"]
    top_sources = [sources[i] for i in I[0]]
    return answer, top_sources

