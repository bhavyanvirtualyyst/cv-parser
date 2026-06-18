import streamlit as st
from src.parser.extractor import extract_pdf
from src.parser.ai_parser import parse_cv


from src.mapper.mapper_loader import map_cv
from src.generator.doc_generator import generate_cv

import os
import json

st.set_page_config(
    page_title="Virtualyyst CV Generator",
    layout="centered"
)

st.title("CV Parser")

file = st.file_uploader(
    "Upload the CV",
    type=["pdf"],
    accept_multiple_files=False
)
template = st.selectbox(
    "Select CV Template",
    [
        "form8",
        "template2",
        "hill"
    ]
)

if file:

    with st.spinner("Extracting CV..."):
        text, image_path = extract_pdf(file)

    st.subheader("Extracted Text")
    st.text_area(
        "CV text",
        text,
        height=200
    )

if st.button("Convert"):

    with st.spinner("Parsing CV..."):
        data = parse_cv(text, template, file.name)

    # st.subheader("Extracted Fields")

    mapped_data = map_cv(
        data,
        template
    )

    # st.json(mapped_data)

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    json_data = json.dumps(
        mapped_data,
        indent=4,
        ensure_ascii=False
    )

    with open(
        "outputs/result.json",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(json_data)

    st.download_button(
        "Download JSON",
        data=json_data,
        file_name="result.json",
        mime="application/json",
        key="json_download"
    )

    with st.spinner("Generating CV..."):
        docx_path = generate_cv(
            mapped_data,
            image_path=image_path,
            template_name=template
        )

    st.success(
        "CV generated successfully"
    )

    with open(docx_path, "rb") as f:

        cv_name = mapped_data.get(
            "expert_name",
            "generated"
        )

        cv_name = cv_name.replace(
            " ",
            "_"
        )

        st.download_button(
            "Download generated CV",
            data=f.read(),
            file_name=f"{cv_name}_cv.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key="cv_download"
        )