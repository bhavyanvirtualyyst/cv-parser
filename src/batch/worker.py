from pathlib import Path
import shutil
import traceback

from src.pipeline.pipeline import run_pipeline

from .config import GENERATED_DIR, FAILED_DIR
from .logger import logger


def process_resume(pdf_path, template="hill"):
    pdf_path = Path(pdf_path)

    try:
        logger.info(f"Processing {pdf_path.name}")

        output_file = run_pipeline(str(pdf_path), template)

        logger.info(f"Successfully generated CV for {pdf_path.name}")

        return {
            "status": "SUCCESS",
            "input": str(pdf_path),
            "output": str(output_file),
            "error": None
        }

    except Exception as e:

        FAILED_DIR.mkdir(parents=True, exist_ok=True)

        shutil.copy2(
            pdf_path,
            FAILED_DIR / pdf_path.name
        )

        logger.error(f"Failed processing {pdf_path.name}")
        logger.error(traceback.format_exc())

        return {
            "status": "FAILED",
            "input": str(pdf_path),
            "output": None,
            "error": str(e)
        }