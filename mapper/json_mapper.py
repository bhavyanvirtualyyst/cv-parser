def map_to_form8(user_json):

    form8 = {}


    # BASIC DETAILS

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

    form8["country_of_citizenship_residence"] = "India"



    # EDUCATION

    education_data = user_json.get(
        "education",
        []
    )


    education_items = []


    if isinstance(education_data, str):

        form8["education"] = education_data


    elif isinstance(education_data, list):

        for edu in education_data:

            if isinstance(edu, dict):

                degree = edu.get("degree", "")
                field = edu.get("field", "")
                university = edu.get("university", "")
                duration = edu.get("duration", "")


                education_text = (
                    f"{degree} "
                    f"{field} "
                    f"{university} "
                    f"{duration}"
                )


                education_items.append(
                    education_text.strip()
                )


            elif isinstance(edu, str):

                education_items.append(
                    edu
                )


        form8["education"] = "\n".join(
            education_items
        )



    # KEY QUALIFICATIONS

    skills = (
        user_json.get("skills")
        or user_json.get("Skills")
        or []
    )


    form8["key_qualifications"] = "\n".join(
        [
            f"• {skill}"
            for skill in skills
        ]
    )



    # EXPERIENCE

    employment_records = []


    for exp in user_json.get("experience", []):


        if isinstance(exp, dict):

            record = {

                "period": exp.get(
                    "duration",
                    ""
                ),

                "organization": exp.get(
                    "company",
                    ""
                ),

                "position": exp.get(
                    "role",
                    ""
                ),

                "location": exp.get(
                    "location",
                    ""
                ),

                "activities": "\n".join(
                    exp.get(
                        "responsibilities",
                        []
                    )
                )
            }


            employment_records.append(
                record
            )


    form8["employment_record"] = employment_records


    return form8