import zipfile
import shutil

from pathlib import Path

from .config import EXTRACTED_DIR


def extract_zip(zip_path):
    if EXTRACTED_DIR.exists():
        shutil.rmtree(EXTRACTED_DIR)

    EXTRACTED_DIR.mkdir(parents=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(EXTRACTED_DIR)
        
    pdfs = []

    for pdf in EXTRACTED_DIR.rglob("*.pdf"):
        pdfs.append(pdf)

    return sorted(pdfs)