import fitz

from src.utils.image_extractor import extract_profile_image


def extract_pdf(pdf_file):
    cv_text = ""
    if hasattr(pdf_file, "read"):
        temp_pdf = "temp_uploaded.pdf"
        with open(temp_pdf, "wb") as f:
            f.write(pdf_file.read())
        pdf_path = temp_pdf
    else:
        pdf_path = pdf_file

    doc = fitz.open(pdf_path)
    for page in doc:
        cv_text += page.get_text()
    image_path = extract_profile_image(doc)
    doc.close()

    return cv_text, image_path