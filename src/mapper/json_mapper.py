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
        r"(\d{1,2})['`/](\d{2,4})",
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


def map_to_form8(user_json):

    form8 = {}

    # PHOTO
    form8["PHOTO"] = ""

    # BASIC DETAILS


    experiences = user_json.get("experience", [])

    if experiences:
        form8["position_title_no"] = experiences[0].get("role", "")

    form8["firm_name"] = ""

    form8["expert_name"] = (
        user_json.get("name")
        or user_json.get("Name")
        or user_json.get("full_name")
        or user_json.get("Full Name")
        or ""
    )

    form8["date_of_birth"] = (
        user_json.get("date_of_birth")
        or user_json.get("dob")
        or user_json.get("DOB")
        or user_json.get("Date of Birth")
        or ""
    )

    form8["years_with_firm"] = ""

    form8["citizenship_residence"] = (
        user_json.get("citizenship")
        or user_json.get("country")
        or "India"
    )

    
    # EDUCATION
     

    education_data = user_json.get("education", [])

    education_items = []


    if isinstance(education_data, str):

        form8["education"] = education_data


    elif isinstance(education_data, list):

        for edu in education_data:

            if isinstance(edu, dict):

                degree = edu.get("degree", "")
                field = edu.get("field", "")
                university = (
                    edu.get("university")
                    or edu.get("institution")
                    or edu.get("college")
                    or ""
                )
                duration = (
                    edu.get("duration")
                    or edu.get("year")
                    or edu.get("years")
                    or ""
                )


                parts = [
                    degree,
                    field,
                    university,
                    duration
                ]


                education_text = ", ".join(
                    [
                        item
                        for item in parts
                        if item
                    ]
                )


                education_items.append(
                    education_text
                )


            elif isinstance(edu, str):

                education_items.append(
                    edu
                )


        form8["education"] = "\n".join(
            education_items
        )


    else:

        form8["education"] = ""
 
    # DETAILED TASKS
    

    tasks = (
        user_json.get("detailed_tasks")
        or user_json.get("responsibilities")
        or []
    )

    if isinstance(tasks, list):

        form8["detailed_tasks"] = "\n".join(
            [
                f"• {task}"
                for task in tasks
            ]
        )

    else:
        form8["detailed_tasks"] = tasks

    
    # KEY QUALIFICATIONS
    

    skills = (
        user_json.get("skills")
        or user_json.get("Skills")
        or []
    )


    if isinstance(skills, list):

        form8["key_qualifications"] = ", ".join(
            skills
        )

    else:

        form8["key_qualifications"] = skills
    
    # EXPERIENCE
    

    employment_records = []

    experiences = (
        user_json.get("experience")
        or user_json.get("work_experience")
        or []
    )


    for exp in experiences:

        if isinstance(exp, dict):

            record = {

                "employment_period":
                    exp.get("period")
                    or exp.get("duration")
                    or "",

                "employment_duration":
                    calculate_duration(
                        exp.get("period")
                        or exp.get("duration")
                        or ""
                    ),


                "employing_organization":
                    exp.get("company")
                    or exp.get("organization")
                    or "",


                "previous_position_held":
                    exp.get("role")
                    or exp.get("position")
                    or "",

                "reference_name": "",
                "reference_position": "",
                "reference_tel": "",
                "reference_email": "",


                "title_of_position_held":
                    exp.get("role")
                    or exp.get("position")
                    or "",


                "assignment_location":
                    exp.get("location")
                    or "",


                "assignment_project_name":
                    exp.get("project")
                    or exp.get("project_name")
                    or "",


                "client":
                    exp.get("client")
                    or "",


                "assignment_year":
                    exp.get("year")
                    or exp.get("duration")
                    or "",


                "main_project_features":
                    exp.get("features")
                    or exp.get("description")
                    or "",


                "activities_performed":
                    exp.get("responsibilities", [])
                    if isinstance(
                        exp.get("responsibilities"),
                        list
                    )
                    else [
                        exp.get("responsibilities", "")
                    ]

            }


            employment_records.append(record)


    form8["employment_record"] = employment_records

    
    # LANGUAGE SKILLS
    

    languages = user_json.get(
        "languages",
        {}
    )

    english = languages.get(
        "english",
        {}
    )


    form8["english_read"] = (
        english.get("read")
        or "Good"
    )


    form8["english_write"] = (
        english.get("write")
        or "Good"
    )


    form8["english_speak"] = (
        english.get("speak")
        or "Good"
    )


    form8["english_remarks"] = (
        english.get("remarks")
        or "NA"
    )

    
    # SIGNING DETAILS
    

    form8["date_of_signing"] = datetime.today().strftime(
        "%d %B %Y"
    )

    return form8