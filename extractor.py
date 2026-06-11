import fitz
import os
import shutil

def extract_pdf(pdf_file):

    # clear previous candidate images
    if os.path.exists("temp/images"):
        shutil.rmtree("temp/images")
    os.makedirs("temp/images", exist_ok=True)


    text = ""

    if hasattr(pdf_file, "read"):

        temp_pdf = "temp_uploaded.pdf"

        with open(temp_pdf, "wb") as f:
            f.write(pdf_file.read())

        pdf_path = temp_pdf

    else:

        pdf_path = pdf_file


    doc = fitz.open(pdf_path)


    for page in doc:
        text += page.get_text()


    os.makedirs("temp/images", exist_ok=True)


    image_path = None
    largest_image = None
    largest_size = 0
    largest_ext = None


    for page in doc:

        for img in page.get_images(full=True):

            xref = img[0]

            extracted = doc.extract_image(xref)

            image_bytes = extracted["image"]
            ext = extracted["ext"]

            print(
                "FOUND IMAGE:",
                len(image_bytes),
                ext
            )


            if len(image_bytes) > largest_size:

                largest_size = len(image_bytes)
                largest_image = image_bytes
                largest_ext = ext


    if largest_image:

        image_path = f"temp/images/profile.{largest_ext}"

        with open(image_path, "wb") as f:
            f.write(largest_image)


    doc.close()


    return text, image_path