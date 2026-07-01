import json
import csv
from datetime import datetime

from .config import REPORT_DIR

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_report(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    success = sum(1 for r in results if r["status"] == "SUCCESS")
    failed = sum(1 for r in results if r["status"] == "FAILED")

    summary = {
        "timestamp": timestamp,
        "total": len(results),
        "success": success,
        "failed": failed,
        "results": results
    }

    json_path = REPORT_DIR / f"batch_report_{timestamp}.json"

    with open(json_path, "w") as f:
        json.dump(summary, f, indent=4)

    csv_path = REPORT_DIR / f"batch_report_{timestamp}.csv"

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["status", "input", "output", "error"]
        )

        writer.writeheader()

        for row in results:
            writer.writerow(row)

    return json_path, csv_path