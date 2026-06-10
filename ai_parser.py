from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROK_API_KEY'))

def parse_cv(text):
    prompt = f"""
Your job is to extract the CV's information
Return ONLY in JSON format

IMPORTANT:
RETURN ONLY VALID JSON
DO NOT WRITE EXPLANATIONS
DO NOT USE MARKDOWN
DO NOT WRAT WITH ``` JSON

Schema:

{{
    "name": "",
    "email": "",
    "phone": "",
    "education": [],
    "experience": [],
    "skills": []
}}

Fields:
name
email
phone
education
experience
skills

the CV is here: {text}
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

    return json.loads(
        response.choices[0].message.content
    )