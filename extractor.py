import fitz


def extract_pdf(file):
    text = ""

    if isinstance(file, str):
        pdf = fitz.open(file)
    else:
        pdf = fitz.open(stream=file.read(),filetype="pdf")

    for page in pdf:
        text += page.get_text()

    pdf.close()
    return text
 
