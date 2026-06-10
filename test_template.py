import json
from pprint import pprint

from mapper.json_mapper import map_to_form8
from generator.doc_generator import generate_cv


with open("sample/sample.json", "r") as file:
    user_json = json.load(file)


print("\n==============================")
print("ORIGINAL EXTRACTED JSON")
print("==============================")

pprint(user_json)


form8_json = map_to_form8(
    user_json
)


print("\n==============================")
print("FORM 8 MAPPED JSON")
print("==============================")

pprint(form8_json)



output_file = generate_cv(
    form8_json
)


print("\n==============================")
print("DOCUMENT GENERATED")
print("==============================")

print(
    output_file
)