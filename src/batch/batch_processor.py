from pathlib import Path

from .zip_handler import extract_zip
from .worker import process_resume
from .report import generate_report
from .logger import logger


def run_batch(zip_path, template="hill"):
    """
    Process every PDF inside a ZIP file.

    Returns:
        results
        json_report_path
        csv_report_path
    """

    zip_path = Path(zip_path)

    logger.info("=" * 60)
    logger.info("Starting Batch Processing")
    logger.info(f"ZIP File: {zip_path}")

    pdf_files = extract_zip(zip_path)

    logger.info(f"Found {len(pdf_files)} PDF(s)")

    results = []

    for index, pdf in enumerate(pdf_files, start=1):

        logger.info(f"[{index}/{len(pdf_files)}] Processing {pdf.name}")

        result = process_resume(
            pdf,
            template
        )

        results.append(result)

    json_report, csv_report = generate_report(results)

    logger.info("Batch Processing Completed")
    logger.info(f"Success : {sum(r['status'] == 'SUCCESS' for r in results)}")
    logger.info(f"Failed  : {sum(r['status'] == 'FAILED' for r in results)}")

    return results, json_report, csv_report