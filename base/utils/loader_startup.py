import os
from django.conf import settings
from .loader import process_and_store

def load_all_pdfs_on_startup():
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    
    if not os.path.exists(upload_dir):
        print("[AutoLoader] Upload directory doesn't exist.")
        return

    print(f"[AutoLoader] Scanning for PDFs in {upload_dir}...")
    for file in os.listdir(upload_dir):
        if file.endswith(".pdf"):
            full_path = os.path.join(upload_dir, file)
            print(f"[AutoLoader] Loading {file}")
            process_and_store(full_path, file)
    print("[AutoLoader] PDF loading complete.")
