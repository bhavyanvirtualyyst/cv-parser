from mapper.json_mapper import map_to_form8

sample_json = {
    "name": "Test User",

    "experience": [
        {
            "company": "ABC Pvt Ltd",
            "role": "Software Engineer",
            "from": "Jan 2022",
            "to": "Jun 2023"
        },
        {
            "company": "XYZ Ltd",
            "role": "Developer",
            "from": "Jul 2023",
            "to": "Present"
        }
    ]
}


result = map_to_form8(sample_json)


for job in result["employment_record"]:
    print(job)