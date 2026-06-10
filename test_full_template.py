from extractor import extract_pdf
from ai_parser import parse_cv
from mapper.json_mapper import map_to_form8
from generator.doc_generator import generate_cv

import pprint


# 1. PDF CV path
pdf_path = "sample/test_cv.pdf"


# 2. Extract raw text
raw_text = extract_pdf(pdf_path)

print("\n================ RAW TEXT ================\n")
print(raw_text[:500])


# 3. AI converts CV text to JSON
parsed_json = parse_cv(raw_text)

print("\n================ AI JSON ================\n")
pprint.pprint(parsed_json)


# 4. Map AI JSON to Form 8 JSON
form8_json = map_to_form8(parsed_json)

print("\n================ FORM 8 JSON ================\n")
pprint.pprint(form8_json)


# 5. Generate DOCX
output = generate_cv(form8_json)


print("\n================ DONE ================\n")
print(output)