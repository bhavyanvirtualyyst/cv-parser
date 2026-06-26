from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_prompt(template_name):
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / f"{template_name}_prompt.md"
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()

def parse_cv(text, template_name, filename):
    prompt_template = load_prompt(template_name)
    prompt = prompt_template.format(cv_text=text, filename=filename)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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
        parsed_data = json.loads(ai_response)

        print("\n========== AI JSON ==========")
        print(json.dumps(parsed_data, indent=4))
        print("=============================\n")

        return parsed_data

    except json.JSONDecodeError:
        print("Invalid JSON returned:")
        print(ai_response)
        return {}

