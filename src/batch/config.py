from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = BASE_DIR / "input"

OUTPUT_DIR = BASE_DIR / "output"

EXTRACTED_DIR = OUTPUT_DIR / "extracted"

GENERATED_DIR = OUTPUT_DIR / "generated"

FAILED_DIR = OUTPUT_DIR / "failed"

LOG_DIR = OUTPUT_DIR / "logs"

REPORT_DIR = OUTPUT_DIR / "reports"

MAX_WORKERS = 4

SUPPORTED_FILES = [".pdf"]