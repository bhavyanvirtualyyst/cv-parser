from docxtpl import DocxTemplate


def generate_cv(data):
    template_path = "templates/form8_template.docx"
    doc = DocxTemplate(template_path)
    doc.render(data)
    output_path = "outputs/final_cv.docx"
    doc.save(output_path)
    return output_path