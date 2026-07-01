import zipfile
import shutil


from pathlib import Path

from .config import EXTRACTED_DIR, SUPPORTED_FILES


def extract_zip(zip_path):
    if EXTRACTED_DIR.exists():
        shutil.rmtree(EXTRACTED_DIR)

    EXTRACTED_DIR.mkdir(parents=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(EXTRACTED_DIR)
        
    pdfs = []

    for file in EXTRACTED_DIR.rglob("*"):

        if "__MACOSX" in file.parts:
            continue

        if file.name.startswith("._"):
            continue

        if file.suffix.lower() not in SUPPORTED_FILES:
            continue

        pdfs.append(file)

    return sorted(pdfs) 