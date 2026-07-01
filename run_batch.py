from pathlib import Path

from src.batch.batch_processor import run_batch


def main():
    zip_file = Path("input/resume.zip")

    #define the template
    template = "hill"

    if not zip_file.exists():
        raise FileNotFoundError(
            f"ZIP file not found: {zip_file}"
        )

    results, json_report, csv_report = run_batch(
        zip_file,
        template
    )

    success = sum(r["status"] == "SUCCESS" for r in results)
    failed = sum(r["status"] == "FAILED" for r in results)

    print("\n========== Batch Complete ==========\n")

    print(f"Total   : {len(results)}")
    print(f"Success : {success}")
    print(f"Failed  : {failed}")

    print(f"\nJSON Report : {json_report}")
    print(f"CSV Report  : {csv_report}")


if __name__ == "__main__":
    main()

