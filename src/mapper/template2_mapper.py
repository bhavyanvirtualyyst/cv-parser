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

        parts.append(
            f"{diff.years} Y"
        )


    if diff.months:

        parts.append(
            f"{diff.months} M"
        )


    return " ".join(parts)


def map_to_template2(data):

    personal = data.get("personal_information", {})

    # -----------------------
    # Education formatting
    # -----------------------
    education_list = []

    for edu in data.get("education", []):
        education_list.append(
            ", ".join(
                filter(
                    None,
                    [
                        edu.get("degree", ""),
                        edu.get("specialization", ""),
                        edu.get("institution", ""),
                        edu.get("year", "")
                    ]
                )
            )
        )

    # -----------------------
    # Employment formatting
    # -----------------------
    employment_record = []

    for exp in data.get("experience", []):

        period = ""

        if exp.get("start_date") or exp.get("end_date"):
            period = f"{exp.get('start_date', '')} - {exp.get('end_date', '')}"

        activities = []

        if exp.get("project_description"):
            activities.append(exp.get("project_description"))

        activities.extend(
            exp.get("responsibilities", [])
        )

        employment_record.append(
            {
                "employment_period": period,

                "employment_duration": exp.get(
                    "duration"
                ) or calculate_duration(
                    period
                ),          

                "employing_organization": exp.get(
                    "company",
                    ""
                ),

                "title_of_position_held": exp.get(
                    "position",
                    ""
                ),

                "location_of_assignment": exp.get(
                    "location",
                    ""
                ),

                "assignment_project_name": exp.get(
                    "project_name",
                    ""
                ),

                "client": exp.get(
                    "client",
                    ""
                ),

                "activities_performed": activities
            }
        )


    # -----------------------
    # Languages
    # -----------------------
    languages = []

    for lang in data.get("languages", []):
        languages.append(
            {
                "name": lang.get("name", ""),
                "reading": lang.get("reading", ""),
                "writing": lang.get("writing", ""),
                "speaking": lang.get("speaking", "")
            }
        )


    # -----------------------
    # Final DOCX context
    # -----------------------
    return {

        "expert_name": personal.get(
            "name",
            ""
        ),

        "position_title_no": data.get(
            "current_position",
            ""
        ),

        "firm_name": data.get(
            "current_company",
            ""
        ),

        "date_of_birth": personal.get(
            "date_of_birth",
            ""
        ),

        "years_with_firm": "",

        "citizenship_residence": personal.get(
            "nationality",
            ""
        ),

        "education": "\n".join(
            education_list
        ),

        "general_work_experience": data.get(
            "total_experience",
            ""
        ),

        "infrastructure_experience": data.get(
            "professional_summary",
            ""
        ),

        "international_experience": "",

        "key_qualifications": "\n".join(
            data.get(
                "skills",
                []
            )
        ),

        "employment_record": employment_record,

        "languages": languages,

        "date": datetime.today().strftime(
            "%d/%m/%Y"
        )
    }