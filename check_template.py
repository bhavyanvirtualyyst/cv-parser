from docxtpl import DocxTemplate


doc = DocxTemplate(
    "templates/form8_template.docx"
)


print(
    doc.get_undeclared_template_variables()
)