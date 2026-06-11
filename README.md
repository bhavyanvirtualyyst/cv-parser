# CV Parser

A Streamlit-based CV parser that extracts text and profile images from PDF resumes, uses Groq AI to convert the CV content into structured JSON, maps that JSON into a Form 8-compatible structure, and generates a filled Word document from a DOCX template.

## What This Project Does

- Uploads a PDF CV through a Streamlit web app.
- Extracts raw text from the PDF with PyMuPDF.
- Extracts the largest embedded image from the PDF as the candidate photo.
- Sends the extracted CV text to a Groq LLM for structured JSON parsing.
- Maps the parsed JSON into Form 8 template fields.
- Generates a final `.docx` CV using the Form 8 Word template.
- Saves JSON and DOCX outputs in the `outputs/` folder.

## Project Structure

```text
CV_parser/
├── app.py                         # Streamlit web interface
├── extractor.py                   # PDF text and image extraction
├── ai_parser.py                   # Groq AI CV-to-JSON parser
├── test_full_template.py          # End-to-end script pipeline
├── requirements.txt               # Python dependencies
├── mapper/
│   └── json_mapper.py             # Converts AI JSON to Form 8 fields
├── generator/
│   └── doc_generator.py           # Renders DOCX from the template
├── templates/
│   ├── form8_template.docx        # Form 8 template
│   └── form8_template_copy.docx   # Template used by the generator
├── sample/
│   └── test_cv.pdf                # Sample PDF for testing
├── outputs/
│   ├── result.json                # Parsed/edited JSON output
│   └── final_cv.docx              # Generated Word document
└── cv_json/
    └── result.json                # Example JSON output
```

## Main Files

### `app.py`

Runs the Streamlit UI. It allows a user to upload a PDF CV, preview the extracted text, parse the CV into fields, download the JSON, and download the generated Form 8 DOCX.

### `extractor.py`

Contains `extract_pdf(pdf_file)`.

It:

- Accepts either an uploaded file object or a local PDF path.
- Extracts all page text with `fitz` from PyMuPDF.
- Finds embedded PDF images.
- Saves the largest image as `temp/images/profile.<extension>`.
- Returns:

```python
(text, image_path)
```

### `ai_parser.py`

Contains `parse_cv(text)`.

It:

- Loads environment variables from `.env`.
- Creates a Groq client using `GROK_API_KEY`.
- Sends the extracted CV text to `llama-3.3-70b-versatile`.
- Requests strict JSON output using a fixed schema.
- Cleans markdown code fences if the model returns them.
- Parses and returns the model response with `json.loads()`.

The expected AI JSON includes:

- Name
- Email
- Phone
- Date of birth
- Current position
- Education
- Skills
- Detailed tasks
- Experience
- Language ability

### `mapper/json_mapper.py`

Contains `map_to_form8(user_json)`.

It converts the AI JSON into the field names expected by the Form 8 DOCX template, including:

- Candidate photo placeholder
- Position title
- Expert name
- Date of birth
- Citizenship/residence
- Education
- Key qualifications
- Detailed tasks
- Employment records
- English language ratings
- Date of signing

### `generator/doc_generator.py`

Contains `generate_cv(data, image_path=None)`.

It:

- Loads `templates/form8_template_copy.docx`.
- Inserts the candidate photo if one was extracted.
- Renders template variables with `docxtpl`.
- Saves the generated file to `outputs/final_cv.docx`.

### `test_full_template.py`

Provides an end-to-end command-line pipeline through `create_cv(pdf_file)`.

Pipeline:

1. Extract PDF text and image.
2. Parse extracted text into AI JSON.
3. Map AI JSON to Form 8 JSON.
4. Generate the final DOCX.

By default, running this file processes:

```text
sample/test_cv.pdf
```

## Requirements

- Python 3.9 or newer
- Groq API key
- PDF CV input
- Form 8 DOCX template

The project uses these key libraries:

- `streamlit`
- `PyMuPDF`
- `groq`
- `python-dotenv`
- `docxtpl`
- `python-docx`

Note: `docxtpl` and `python-docx` are imported by the generator. If they are not already installed in your environment, install them manually even if they are missing from `requirements.txt`.

## Setup

### 1. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install docxtpl python-docx
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROK_API_KEY=your_groq_api_key_here
```

Important: The code currently reads `GROK_API_KEY` from the environment. Keep this spelling unless you update `ai_parser.py`.

## Running the Streamlit App

Start the web app:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

Usage:

1. Upload a PDF CV.
2. Review the extracted text.
3. Click `Convert`.
4. Review/edit extracted fields.
5. Download the JSON file.
6. Download the generated Form 8 DOCX.

## Running the Full Pipeline from Terminal

Run:

```bash
python test_full_template.py
```

This processes:

```text
sample/test_cv.pdf
```

Generated output:

```text
outputs/final_cv.docx
```

To process another PDF, update the file path in `test_full_template.py`:

```python
create_cv("sample/test_cv.pdf")
```

Replace it with your desired PDF path.

## Data Flow

```text
PDF CV
  ↓
extractor.py
  ↓
Raw text + candidate image
  ↓
ai_parser.py
  ↓
Structured AI JSON
  ↓
mapper/json_mapper.py
  ↓
Form 8 template JSON
  ↓
generator/doc_generator.py
  ↓
outputs/final_cv.docx
```

## Output Files

### `outputs/result.json`

Stores the parsed CV fields from the Streamlit workflow.

### `outputs/final_cv.docx`

Stores the generated Form 8 CV document.

### `temp/images/profile.<extension>`

Stores the extracted candidate image. The `temp/` directory is ignored by Git.

### `temp_uploaded.pdf`

Temporary copy of an uploaded PDF. This file is ignored by Git.

## Template Notes

The generator uses:

```text
templates/form8_template_copy.docx
```

The DOCX template should contain placeholders that match the keys created in `mapper/json_mapper.py`, such as:

- `PHOTO`
- `position_title_no`
- `expert_name`
- `date_of_birth`
- `education`
- `key_qualifications`
- `detailed_tasks`
- `employment_record`
- `english_read`
- `english_write`
- `english_speak`
- `english_remarks`
- `date_of_signing`

If a template variable does not appear in the generated DOCX, check that the placeholder name in the Word template exactly matches the mapped key.

## Troubleshooting

### `ModuleNotFoundError: No module named 'docxtpl'`

Install the missing DOCX rendering packages:

```bash
pip install docxtpl python-docx
```

### `GroqError` or authentication errors

Check that your `.env` file exists and contains:

```env
GROK_API_KEY=your_groq_api_key_here
```

Also confirm that the key is valid and has access to the selected Groq model.

### JSON parsing fails

The AI response must be valid JSON. If parsing fails:

- Print `ai_response` in `ai_parser.py`.
- Check whether the model returned extra text.
- Confirm the CV text is not empty.
- Reduce overly long or noisy PDF input if needed.

### No photo appears in the generated DOCX

Possible causes:

- The PDF does not contain an embedded image.
- The candidate image is not the largest image in the PDF.
- The image extraction step did not create `temp/images/profile.<extension>`.
- The DOCX template is missing the `PHOTO` placeholder.

### Streamlit extracted text looks unusual

`extract_pdf()` returns both text and image path as a tuple:

```python
(text, image_path)
```

If the Streamlit text preview shows tuple-like output, unpack it in `app.py`:

```python
text, image_path = extract_pdf(file)
```

The command-line pipeline in `test_full_template.py` already unpacks this correctly.

## Git Ignore Notes

The repository ignores:

```text
venv
.env
temp
temp_uploaded.pdf
```

This keeps local environments, secrets, temporary images, and uploaded PDF copies out of version control.

## Security Notes

- Do not commit `.env` or API keys.
- Uploaded CVs may contain personal data, so handle input and output files carefully.
- Generated JSON and DOCX files may also contain personal information.
- Review AI-generated fields before sharing the final document.

## Current Limitations

- Only PDF upload is supported in the Streamlit app.
- The parser depends on an external Groq API call.
- AI output quality depends on the clarity of the input CV.
- The image extraction logic chooses the largest embedded image, which may not always be the profile photo.
- The app currently saves output files to fixed paths in `outputs/`.
- Some sample/output files are committed and may need cleanup before production use.

## Suggested Improvements

- Add `docxtpl` and `python-docx` to `requirements.txt`.
- Unpack `extract_pdf()` correctly in `app.py`.
- Add validation for the AI JSON response.
- Add support for DOCX CV input.
- Add a configurable output filename.
- Add unit tests for the mapper.
- Add error handling around missing templates, missing API keys, and invalid PDFs.
