from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os


def generate_cv(data, image_path=None):
    print("IMAGE PATH RECEIVED:", image_path)
    template_path = "templates/form8_template_copy.docx"

    doc = DocxTemplate(template_path)

    if image_path and os.path.exists(image_path):
        data["PHOTO"] = InlineImage(
            doc,
            image_path,
            width=Mm(35),
            height=Mm(40)
        )
    else:
        data["PHOTO"] = ""

    doc.render(data)

    # Fix Word mobile / WhatsApp rendering issues
    document = doc.docx

    for table in document.tables:
        table.allow_autofit = True

        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()

            for child in list(trPr):
                if child.tag.endswith('trHeight'):
                    trPr.remove(child)

    output_path = "outputs/final_cv.docx"
    doc.save(output_path)

    return output_path