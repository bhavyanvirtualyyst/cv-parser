from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os
import html
import copy
from pathlib import Path

def escape_xml(data):
    if isinstance(data, dict):
        return {
            key: escape_xml(value)
            for key, value in data.items()
        }

    elif isinstance(data, list):
        return [
            escape_xml(item)
            for item in data
        ]

    elif isinstance(data, str):
        return html.escape(data)

    return data

def generate_cv(data, image_path=None, template_name='form8'):
    data = copy.deepcopy(data)
    BASE_DIR = Path(__file__).resolve().parents[2]
    template_path = BASE_DIR/"templates"/f"{template_name}_template.docx"
    doc = DocxTemplate(template_path)
    if image_path and os.path.exists(image_path):
        data["PHOTO"] = InlineImage(doc, image_path, width=Mm(35), height=Mm(40))
    else:
        data["PHOTO"] = ""
    data = escape_xml(data)
    doc.render(data)

    # fixed lightweight rendering issues (mobiles & tablets)
    document = doc.docx
    for table in document.tables:
        table.allow_autofit = True
        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            for child in list(trPr):
                if child.tag.endswith('trHeight'):
                    trPr.remove(child)


    name = data.get('expert_name') or data.get('name') or 'final_cv'
    first_name = name.split()[0]
    output_path = BASE_DIR / "outputs" / f"{first_name}_CV.docx"

    output_path.parent.mkdir(exist_ok=True)
    doc.save(output_path)

    return output_path