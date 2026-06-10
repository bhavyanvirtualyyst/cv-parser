import streamlit as st
from extractor import extract_pdf
from ai_parser import parse_cv

from docxtpl import DocxTemplate
import os
import json
import base64


st.title("CV Parser")


TEMPLATE_PATH = "CV_Form 8_Template.docx"


file = st.file_uploader(
    "Upload the CV",
    type=["pdf"],
    accept_multiple_files=False
)


def generate_docx(data):

    doc = DocxTemplate(TEMPLATE_PATH)

    doc.render(data)

    os.makedirs("cv_json", exist_ok=True)

    output_path = "cv_json/generated_cv.docx"

    doc.save(output_path)

    return output_path


if file:

    print("Extracting started...")

    text = extract_pdf(file)

    print("Extracted successfully!")

    st.subheader("Extracted text")

    st.text_area(
        "CV text",
        text,
        height=200
    )


    if st.button("Convert"):

        print("Parsing JSON...")

        data = parse_cv(text)

        print("Parsed successfully!")

        st.subheader("Extracted fields")

        edited = {}

        for key, value in data.items():

            edited[key] = st.text_input(
                key,
                value
            )


        # SAVE JSON

        os.makedirs("cv_json", exist_ok=True)

        json_path = "cv_json/result.json"

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                edited,
                f,
                indent=4,
                ensure_ascii=False
            )


        st.download_button(
            "Download JSON",
            data=json.dumps(
                edited,
                indent=4
            ),
            file_name="result.json",
            mime="application/json"
        )


        # GENERATE CV TEMPLATE

        docx_path = generate_docx(
            edited
        )


        with open(docx_path, "rb") as f:

            st.download_button(
                "Download Filled CV",
                data=f,
                file_name="generated_cv.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )


        # DOCX PREVIEW

        st.subheader(
            "Generated CV Preview"
        )


        with open(
            docx_path,
            "rb"
        ) as f:

            encoded = base64.b64encode(
                f.read()
            ).decode()


        st.markdown(
            f"""
            <iframe 
            src="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{encoded}"
            width="100%"
            height="800">
            </iframe>
            """,
            unsafe_allow_html=True
        )