from src.parser.extractor import extract_pdf
from src.parser.ai_parser import parse_cv
from src.generator.doc_generator import generate_cv as generator
import pprint


def get_mapper(template):
    if template == "form8":
        from src.mapper.form8_mapper import map_to_form8
        return map_to_form8

    elif template == "template2":
        from src.mapper.template2_mapper import map_to_template2
        return map_to_template2

    elif template == "hill":
        from src.mapper.hill_mapper import map_to_hill
        return map_to_hill

    else:
        raise ValueError(f"Unknown template: {template}")


def run_pipeline(pdf_path, template="hill"):
    print("\n========== STEP 1 : EXTRACT ==========\n")

    raw_text, image_path = extract_pdf(pdf_path)

    mapper = get_mapper(template)

    print("Image:", image_path)
    print("\nRaw Text Preview:\n")
    print(raw_text[:1000])

    print("\n========== STEP 2 : AI PARSER ==========\n")

    parsed_json = parse_cv(raw_text, template, pdf_path)

    pprint.pprint(parsed_json)

    print("\n========== STEP 3 : MAPPER ==========\n")

    mapped_json = mapper(parsed_json)

    pprint.pprint(mapped_json)

    print("\n========== STEP 4 : DOCX GENERATOR ==========\n")

    output_file = generator(
        mapped_json,
        image_path,
        template
    )

    print("\nGenerated CV:")
    print(output_file)

    return output_file


if __name__ == "__main__":
    run_pipeline(
        "data/sample/kiran_test.pdf",
        "hill"
    )