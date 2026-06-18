from datetime import datetime

from src.utils.date_utils import calculate_duration


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