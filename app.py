import streamlit as st
from src.parser.extractor import extract_pdf
from src.parser.ai_parser import parse_cv
# from test_full_template import create_cv

from src.mapper.json_mapper import map_to_form8
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
            data = parse_cv(text)
        st.subheader("Extracted Fields")
        mapped_data = map_to_form8(data)
        st.json(mapped_data)
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
            mime="application/json"
        )


        # Generate Form 8 DOCX using working pipeline

        with st.spinner("Generating Form 8 CV..."):

            # file.seek(0)

            # docx_path = create_cv(
            #     file
            # )

            docx_path = generate_cv(
                mapped_data,
                image_path=image_path
            )


        st.success(
            "CV generated successfully"
        )


        # Download DOCX

        with open(
            docx_path,
            "rb"
        ) as f:

                with open(
                    docx_path,
                    "rb"
                ) as f:

                        cv_name = mapped_data.get("expert_name", "generated")
                        cv_name = cv_name.replace(" ", "_")
                        st.download_button(
                            "Download generated CV",
                            data=f.read(),
                            file_name=f"{cv_name}_cv.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )