from extractor import extract_pdf
from ai_parser import parse_cv
from mapper.json_mapper import map_to_form8
from generator.doc_generator import generate_cv

import pprint


def create_cv(pdf_file):

    # 1. Extract raw text + image
    raw_text, image_path = extract_pdf(pdf_file)

    print("EXTRACTED IMAGE:", image_path)


    print("\n================ RAW TEXT ================\n")
    print(raw_text[:500])


    # 2. AI converts CV text to JSON
    parsed_json = parse_cv(raw_text)


    print("\n================ AI JSON ================\n")
    pprint.pprint(parsed_json)


    # 3. Map AI JSON to Form 8 JSON
    form8_json = map_to_form8(parsed_json)


    print("\n================ FORM 8 JSON ================\n")
    pprint.pprint(form8_json)


    # 4. Generate DOCX
    output = generate_cv(
        form8_json,
        image_path
    )


    print("\n================ DONE ================\n")
    print(output)


    return output



if __name__ == "__main__":

    create_cv(
        "sample/test_cv.pdf"
    )