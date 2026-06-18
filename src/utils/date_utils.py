from datetime import datetime
from dateutil.relativedelta import relativedelta
import re


def calculate_duration(period):

    if not period:
        return ""

    period = period.lower()

    month_map = {
        "jan": 1,
        "january": 1,
        "feb": 2,
        "february": 2,
        "mar": 3,
        "march": 3,
        "apr": 4,
        "april": 4,
        "may": 5,
        "jun": 6,
        "june": 6,
        "jul": 7,
        "july": 7,
        "aug": 8,
        "august": 8,
        "sep": 9,
        "sept": 9,
        "september": 9,
        "oct": 10,
        "october": 10,
        "nov": 11,
        "november": 11,
        "dec": 12,
        "december": 12
    }

    numeric_dates = re.findall(
        r"(\d{1,2})['`/\-](\d{2,4})",
        period
    )

    dates = []

    for month, year in numeric_dates:

        year = int(year)

        if year < 100:
            year += 2000

        dates.append(
            datetime(
                year,
                int(month),
                1
            )
        )

    word_dates = re.findall(
        r"([a-z]+)\s+(\d{4})",
        period
    )

    for month, year in word_dates:

        if month in month_map:
            dates.append(
                datetime(
                    int(year),
                    month_map[month],
                    1
                )
            )

    if not dates:
        return ""

    start_date = dates[0]

    if (
        "till date" in period
        or "till now" in period
        or "to date" in period
        or "present" in period
        or "current" in period
        or "currently" in period
        or "ongoing" in period
        or "now" in period
    ):
        end_date = datetime.today()

    else:
        end_date = dates[-1]

    diff = relativedelta(
        end_date,
        start_date
    )

    parts = []

    if diff.years:
        parts.append(f"{diff.years} Y")

    if diff.months:
        parts.append(f"{diff.months} M")

    return " ".join(parts)