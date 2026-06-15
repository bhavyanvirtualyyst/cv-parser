import os
import shutil


def extract_profile_image(doc):
    if os.path.exists("temp/images"):
        shutil.rmtree("temp/images")
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
            if len(image_bytes) > largest_size:
                largest_size = len(image_bytes)
                largest_image = image_bytes
                largest_ext = ext

    if largest_image:
        image_path = f"temp/images/profile.{largest_ext}"
        with open(image_path, "wb") as f:
            f.write(largest_image)

    return image_path