# import streamlit as st
# from extractor import extract_pdf
# from ai_parser import parse_cv
# import os
# import json

# st.title('CV Parser')

# file = st.file_uploader('Upload the CV', type=["pdf"], accept_multiple_files=False)

# if file:

#     print("Extracting started...")

#     #extracts pdf to raw text
#     text = extract_pdf(file)
    
#     print("Extracted text successfully!", text)
    
#     st.subheader("Extracted text")
#     st.text_area("CV text", text, height=200)

#     if st.button("Convert"):

#         print("Parsing to json...")

#         #parses the text to json format
#         data = parse_cv(text)

#         print("Parsed successfully!")

#         st.subheader("Extracted fields successfully!")
#         edited = {}
#         for key, value in data.items():
#             edited[key] = st.text_input(key, value)

#         # ***DOWNLOADING***
        
#         #create the output folder, ignores if already done
#         os.makedirs("output", exist_ok=True)
#         path = "output/result.json"
        
#         #save json at 'path'
#         with open(path, 'w', encoding='utf-8') as f:
#             json.dump(data, f, indent=4, ensure_ascii=False)

#         st.success(f'JSON saved successfully at {path}')

#         #option to download
#         st.download_button("Download JSON", data=json.dumps(data, indent=4), file_name="result.json", mime="applicahotion/json")

# import streamlit as st
# from extractor import extract_pdf
# from ai_parser import parse_cv
# import os
# import json
# import base64

# st.title('CV Parser')

# file = st.file_uploader(
#     'Upload the CV',
#     type=["pdf"],
#     accept_multiple_files=False
# )

# if file:

#     print("Extracting started...")

#     # extracts pdf to raw text
#     text = extract_pdf(file)

#     print("Extracted text successfully!", text)

#     st.subheader("Extracted text")
#     st.text_area("CV text", text, height=200)

#     if st.button("Convert"):

#         print("Parsing to json...")

#         # parses the text to json format
#         data = parse_cv(text)

#         print("Parsed successfully!")

#         st.subheader("Extracted fields successfully!")

#         edited = {}

#         for key, value in data.items():
#             edited[key] = st.text_input(key, value)

#         # ***DOWNLOADING***

#         # create the output folder, ignores if already done
#         os.makedirs("output", exist_ok=True)

#         path = "output/result.json"

#         # save edited json at 'path'
#         with open(path, 'w', encoding='utf-8') as f:
#             json.dump(edited, f, indent=4, ensure_ascii=False)

#         st.success(f'JSON saved successfully at {path}')

#         # option to download edited JSON
#         st.download_button(
#             "Download JSON",
#             data=json.dumps(edited, indent=4),
#             file_name="result.json",
#             mime="application/json"
#         )

#         # ***PDF PREVIEW***

#         st.subheader("PDF Preview")

#         # reset file pointer
#         file.seek(0)

#         # convert PDF to base64
#         base64_pdf = base64.b64encode(file.read()).decode("utf-8")

#         # show PDF iframe
#         pdf_display = f"""
#         <iframe
#             src="data:application/pdf;base64,{base64_pdf}"
#             width="100%"
#             height="700px"
#             type="application/pdf">
#         </iframe>
#         """

#         st.markdown(
#             pdf_display,
#             unsafe_allow_html=True
#         )



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

    os.makedirs("output", exist_ok=True)

    output_path = "output/generated_cv.docx"

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

        os.makedirs("output", exist_ok=True)

        json_path = "output/result.json"

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