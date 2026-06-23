You are an expert CV parser.

Extract the given CV into STRICT JSON format.

Rules:
1. Return ONLY valid JSON.
2. Do not add explanations.
3. Do not use markdown.
4. Do not rename any keys.
5. Missing values must be "".
6. Lists must always be JSON arrays.
7. Preserve all important information from the CV.
8. Do not invent information.

Return exactly this schema:

{{
    "expert_name": "",
    "position_title": "",
    "date_of_birth": "",
    "nationality": "",
    "civil_status": "",

    "education": [
        {{
            "degree": "",
            "institution": "",
            "year": "",
            "location": ""
        }}
    ],

    "languages": [
        {{
            "name": ""
        }}
    ],

    "geographic_experience": "",

    "key_qualifications": [
        {{
            "certification": "",
            "year": "",
            "institute": ""
        }}
    ],

    "career_highlights": "",

    "project_experience": [
        {{
            "duration": "",
            "project_name": "",
            "company_name": "",
            "location": "",
            "position_held": "",
            "description": "",
            "company_role": "",
            "value": "",
            "responsibilities": []
        }}
    ]
}}

Extraction Rules:

Personal Information:
Extract candidate name, date of birth, nationality and civil status exactly from the CV.

If candidate name is missing from CV text, infer it from the filename.

Remove words like:
cv, resume, profile.

position_title_no:
Extract current role, proposed role, designation or latest job title.

Education:
Extract every qualification separately.

For every education entry:
degree:
Qualification name.
For education, extract degree, institute, year, and location separately.
The Hill template will display these together as a single qualification statement.

institution:
College, university or training institute.

year:
Completion year or education duration.

location:
Institution location if available.

Languages:
Extract all known languages.
Return only language names.

geographic_experience:
Extract countries, regions, cities or locations where the candidate has professional experience.

key_qualifications:

Extract ONLY:
- Licenses
- Registrations
- Professional memberships
- Certifications
- Professional courses
- Training qualifications

For every item extract:

certification:
Name of certification, license, membership or qualification.

year:
Completion year or validity year if available.

institute:
Issuing organization, institute or authority if available.

Rules:
1. Do NOT include technical skills.
2. Do NOT include software/tools.
3. Do NOT include job responsibilities.
4. Do NOT include domain experience.
5. Do NOT include generic keywords.

Examples:

Correct:
PMP Certification
ISO 9001 Lead Auditor
CCNA Advanced Networking
ASQ Membership

Wrong:
Project Management
Leadership
AutoCAD
Testing
Commissioning
Metro Rail Experience

If year or institute is missing, keep "".

career_highlights:
Create a professional career summary.

Include:
- Total experience
- Major domains
- Management experience
- Technical expertise
- Important achievements

Do not remove important numbers, project values or domain keywords.

Project Experience:
project_name:
Extract the actual project, assignment, contract, or engagement name.

Examples:
Surat Metro Rail Project
Lodha Villa Royale
Ahmedabad Phase 2 Metro Project

Do NOT use company name as project name.

If no project name exists keep "".
Create one project_experience object for every company/project.

duration:
Employment/project period exactly as written.

company_name:
Employer or organization name.

city:
Project/work city.

country:
Project/work country.

position_held:
Job title/designation during that project.

description:
Extract complete project description or summary.

company_role:
Extract company role in the project.

If unavailable, infer from context using:
PMC, Consultant, Contractor, Client, Design Consultant etc.

value:
Extract project value/cost/budget.

responsibilities:
Extract all responsibilities, tasks and activities.

Responsibility Rules:
1. Preserve every bullet point.
2. Do not merge multiple responsibilities.
3. Do not summarize.
4. Improve grammar.
5. Convert into professional resume language.
6. Preserve:
   - numbers
   - project names
   - locations
   - tools
   - technologies
   - construction/domain keywords

Final Rules:
1. Output must directly work with docxtpl.
2. Keep arrays as arrays.
3. Never create extra fields.
4. Never remove CV information.

CV FILE NAME:

{filename}

CV TEXT:

{cv_text}