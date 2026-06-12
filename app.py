import streamlit as st
from extractor import extract_pdf
from ai_parser import parse_cv
# from test_full_template import create_cv

from mapper.json_mapper import map_to_form8
from generator.doc_generator import generate_cv

import os
import json


st.title("CV Parser")


file = st.file_uploader(
    "Upload the CV",
    type=["pdf"],
    accept_multiple_files=False
)


if file:


    # Extract preview text

    with st.spinner("Extracting CV..."):

        text, image_path = extract_pdf(file)


    st.subheader("Extracted Text")

    st.text_area(
        "CV text",
        text,
        height=200
    )


    if st.button("Convert"):


        # AI JSON preview

        with st.spinner("Parsing CV..."):

            data = parse_cv(text)


        st.subheader("Extracted Fields")


        # edited = {}

        # for key, value in data.items():

        #     edited[key] = st.text_input(
        #         key,
        #         str(value)
        #     )

        # new
        mapped_data = map_to_form8(data)
        st.json(mapped_data)


        # Save JSON

        os.makedirs(
            "outputs",
            exist_ok=True
        )


        json_data = json.dumps(
            mapped_data,            # edited from 'edited'
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

            st.download_button(
                "Download Filled CV",
                data=f.read(),
                file_name="generated_cv_streamlit.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )