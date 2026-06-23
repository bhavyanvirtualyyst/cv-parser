from src.utils.date_utils import calculate_duration


def map_to_hill(data):

    # -----------------------
    # Education formatting
    # -----------------------
    education = []

    for edu in data.get("education", []):

        qualification = ", ".join(
            filter(
                None,
                [
                    edu.get("degree", ""),
                    edu.get("institution", ""),
                    edu.get("year", "")
                ]
            )
        )

        education.append(qualification)
    # -----------------------
    # Languages formatting
    # -----------------------
    languages = []

    for lang in data.get("languages", []):
        languages.append(
            {
                "name": lang.get(
                    "name",
                    ""
                )
            }
        )


    # -----------------------
    # Project Experience formatting
    # -----------------------
    project_experience = []

    for project in data.get("project_experience", []):

        duration = project.get(
            "duration",
            ""
        )

        project_experience.append(
            {
                "duration": duration,

                "project_name": project.get(
                    "project_name",
                    ""
                ),

                "company_name": project.get(
                    "company_name",
                    ""
                ),

                "location": project.get(
                    "location",
                    ""
                ),                

                "position_held": project.get(
                    "position_held",
                    ""
                ),

                "description": project.get(
                    "description",
                    ""
                ),

                "company_role": project.get(
                    "company_role",
                    ""
                ),

                "value": project.get(
                    "value",
                    ""
                ),

                "responsibilities": project.get(
                    "responsibilities",
                    []
                )
            }
        )

    # -----------------------
    # Key Qualifications formatting
    # -----------------------
    key_qualifications = []

    for item in data.get("key_qualifications", []):

        qualification = ", ".join(
            filter(
                None,
                [
                    item.get("certification", ""),
                    item.get("year", ""),
                    item.get("institute", "")
                ]
            )
        )

        key_qualifications.append(qualification)

    # -----------------------
    # Final DOCX context
    # -----------------------
    return {

        "expert_name": data.get(
            "expert_name",
            ""
        ),

        "position_title_no": data.get(
            "position_title_no",
            ""
        ),

        "date_of_birth": data.get(
            "date_of_birth",
            ""
        ),

        "nationality": data.get(
            "nationality",
            ""
        ),

        "civil_status": data.get(
            "civil_status",
            ""
        ),

        "education": education,

        "languages": languages,

        "geographic_experience": data.get(
            "geographic_experience",
            ""
        ),

        "key_qualifications": key_qualifications,

        "career_highlights": data.get(
            "career_highlights",
            ""
        ),

        "project_experience": project_experience
    }
