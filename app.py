import streamlit as st
from extractor import extract_pdf
from ai_parser import parse_cv
import os
import json

st.title('CV Parser')

file = st.file_uploader('Upload the CV', type=["pdf"], accept_multiple_files=False)

if file:

    print("Extracting started...")

    #extracts pdf to raw text
    text = extract_pdf(file)
    
    print("Extracted text successfully!", text)
    
    st.subheader("Extracted text")
    st.text_area("CV text", text, height=200)

    if st.button("Convert"):

        print("Parsing to json...")

        #parses the text to json format
        data = parse_cv(text)

        print("Parsed successfully!")

        st.subheader("Extracted fields successfully!")
        # edited = {}
        # for key, value in data.items():
        #     edited[key] = st.text_input(key, value)

        # ***DOWNLOADING***
        
        #create the output folder, ignores if already done
        os.makedirs("output", exist_ok=True)
        path = "output/result.json"
        
        #save json at 'path'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        st.success(f'JSON saved successfully at {path}')

        #option to download
        st.download_button("Download JSON", data=json.dumps(data, indent=4), file_name="result.json", mime="applicahotion/json")