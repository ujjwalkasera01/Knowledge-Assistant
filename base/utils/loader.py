import os
import hashlib
import json
import fitz  # PyMuPDF
from .embedding import embed_and_store, save_vector_store

PROCESSED_JSON = "processed_files.json"

def load_processed_files():
    if os.path.exists(PROCESSED_JSON):
        with open(PROCESSED_JSON, "r") as f:
            return json.load(f)
    return {}

def save_processed_files(data):
    with open(PROCESSED_JSON, "w") as f:
        json.dump(data, f)

def file_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def should_process_pdf(filepath, processed_data):
    fname = os.path.basename(filepath)
    return processed_data.get(fname) != file_hash(filepath)

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    print(f"[DEBUG] Extracted text from PDF: {len(text)} characters")
    return text

def process_and_store(file_path, doc_title):
    print(f"[DEBUG] Processing and storing file: {file_path} - {doc_title}")
    text = extract_text_from_pdf(file_path)
    embed_and_store(text, doc_title)
    
    print(f"[DEBUG] Completed embedding for: {doc_title}")

def autoload_pdfs(upload_dir="media/uploads"):
    from .embedding import load_vector_store  # Make sure to use the updated store
    global corpus_chunks, sources, index  # important: use existing memory vars

    # Load existing chunks into memory
    corpus_chunks, sources, index, _ = load_vector_store()

    processed = load_processed_files()

    for filename in os.listdir(upload_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        path = os.path.join(upload_dir, filename)

        if should_process_pdf(path, processed):
            print(f"[AutoLoader] Processing: {filename}")
            process_and_store(path, filename)
            processed[filename] = file_hash(path)
        else:
            print(f"[AutoLoader] Skipping already processed: {filename}")

    save_processed_files(processed)


