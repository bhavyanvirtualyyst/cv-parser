from groq import Groq
import json
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def load_prompt():
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "form8_prompt.md"
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()

def parse_cv(text):
    prompt_template = load_prompt()
    prompt = prompt_template.format(cv_text=text)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )
    ai_response = response.choices[0].message.content
    ai_response = (
        ai_response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
    try:
        return json.loads(ai_response)
    except json.JSONDecodeError:
        print("Invalid JSON returned:")
        print(ai_response)
        return {}