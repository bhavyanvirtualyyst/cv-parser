from groq import Groq
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv('GROK_API_KEY'))

def parse_cv(text):
    prompt = f"""
You are an expert CV parser.

Extract the following CV text into STRICT JSON format.

Rules:
1. Return ONLY valid JSON.
2. Do not add explanations.
3. Do not use markdown.
4. Do not rename any keys.
5. If data is missing, use an empty string "".
6. Lists must be real JSON arrays, not strings.

Return exactly this schema:

{{
    "name": "",
    "email": "",
    "phone": "",
    "date_of_birth": "",
    "current_position": "",

    "education": [
        {{
            "degree": "",
            "field": "",
            "university": "",
            "duration": ""
        }}
    ],

    "skills": [],

    "detailed_tasks": [],

    "experience": [
        {{
            "company": "",
            "role": "",
            "duration": "",
            "total_duration": "",
            "location": "",
            "projectName": "",
            "client": "",
            "features": "",
            "responsibilities": [],
            "achievements": []
        }}
    ],

    "languages": {{
        "english": {{
            "read": "",
            "write": "",
            "speak": "",
            "remarks": ""
        }}
    }}
}}

Extraction rules:

Education:
Extract all degrees, universities and years.

Skills:
Extract technical skills, management skills, languages, certifications.

Experience:
Create one object for every job/project.

company:
Employer name.

role:
Job title.

duration:
Original employment period exactly as written.
Example: "09'19-09'24"

total_duration:
Only calculate if explicitly available.
Otherwise keep empty.

location:
Work location.

projectName:
Project or assignment name.

client:
Client/customer name.

features:
Main project details.

responsibilities:
Extract all activities performed, duties and tasks.

achievements:
Extract measurable achievements.

Language Extraction Rules:

Extract English language ability.

For English:
read:
Return "Good", "Average", or "Poor"

write:
Return "Good", "Average", or "Poor"

speak:
Return "Good", "Average", or "Poor"

remarks:
Any additional information.
If no remarks are available, return "NA".

If English is mentioned as a known language but skill level is not specified, assume:
read = "Good"
write = "Good"
speak = "Good"
remarks = "NA"

For date_of_signing:
Use today's date if not available in the CV.
Format: DD Month YYYY

In the activities and project sections:
1. DO NOT summarize, shorten, merge, or rewrite project descriptions and responsibilities.
2. Preserve every activity, responsibility, achievement, and bullet point from the original CV.
3. Extract project features and activities exactly as mentioned in the CV.
4. Only make these changes:
   - Fix grammar mistakes
   - Convert sentences into professional resume-style tone
   - Maintain consistent tense
5. Do not invent new information.
6. Do not remove technical details, numbers, tools, technologies, locations, or project names. ALWAYS mention the keywords in the output.
7. If the original CV contains multiple bullet points under a project or job, keep them as separate bullet points.
8. The final output should contain the same level of detail as the source CV.


CV TEXT:

{text}
"""

    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        temperature = 0
    )

    ai_response = response.choices[0].message.content

    # print("\nAI response starts.")
    # print(repr(ai_response))
    # print("AI response ends here.\n")

    ai_response = (
        ai_response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(ai_response)