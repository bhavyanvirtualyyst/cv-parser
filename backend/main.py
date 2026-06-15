from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
import shutil


from src.parser.extractor import extract_pdf
from src.parser.ai_parser import parse_cv
from src.generator.doc_generator import generate_cv



app = FastAPI()



# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)



@app.get("/")
def home():

    return {
        "message": "Virtualyyst CV API running"
    }




@app.post("/convert")
async def convert_cv(file: UploadFile = File(...)):


    temp_folder = Path("temp/uploads")

    temp_folder.mkdir(
        parents=True,
        exist_ok=True
    )


    input_path = temp_folder / file.filename



    # save uploaded PDF
    with open(input_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )



    # PDF extraction

    cv_text, image_path = extract_pdf(
        input_path
    )



    # AI parsing

    data = parse_cv(
        cv_text
    )



    # DOCX generation

    output_file = generate_cv(
        data,
        image_path
    )



    return FileResponse(
        output_file,

        filename=output_file.name,

        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )