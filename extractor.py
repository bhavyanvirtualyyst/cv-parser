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
 
# import fitz
# import os


# def extract_pdf(pdf_file):

#     text = ""

#     temp_pdf = "temp_uploaded.pdf"

#     with open(temp_pdf, "wb") as f:
#         f.write(pdf_file.read())


#     doc = fitz.open(temp_pdf)


#     # Extract text
#     for page in doc:
#         text += page.get_text()


#     # Extract image
#     image_path = None

#     os.makedirs("temp/images", exist_ok=True)

#     for page_index in range(len(doc)):

#         page = doc[page_index]
#         images = page.get_images()

#         for img_index, img in enumerate(images):

#             xref = img[0]
#             base_image = doc.extract_image(xref)

#             image_bytes = base_image["image"]
#             ext = base_image["ext"]

#             image_path = f"temp/images/profile.{ext}"

#             with open(image_path, "wb") as img_file:
#                 img_file.write(image_bytes)

#             break

#         if image_path:
#             break


#     doc.close()

#     os.remove(temp_pdf)

#     return text, image_path