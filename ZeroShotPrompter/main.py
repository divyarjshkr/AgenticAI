import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in your .env file.")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"


def classify_complaint(complaint):
    prompt = f"""
You are a customer complaint urgency classifier.

Classify the following customer complaint as exactly one of:
- Urgent
- Not Urgent

Rules:
- Urgent: Critical problems requiring immediate attention, such as
  payment system outages, security issues, or serious financial problems.
- Not Urgent: Routine issues, minor delays, product complaints, or
  problems that do not require immediate attention.

Return only valid JSON in this format:
{{
    "classification": "Urgent or Not Urgent",
    "reason": "Brief explanation"
}}

Customer complaint:
{complaint}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_completion_tokens=200
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The API returned an empty response.")

    content = content.strip()

    # Remove Markdown code fences if present
    if content.startswith("```"):
        lines = content.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    result = json.loads(content)

    if not isinstance(result, dict):
        raise ValueError("The model response must be a JSON object.")

    if result.get("classification") not in ("Urgent", "Not Urgent"):
        raise ValueError("The model returned an invalid classification.")

    if not isinstance(result.get("reason"), str):
        raise ValueError("The model did not return a valid reason.")

    return result


def main():
    print("CUSTOMER COMPLAINT CLASSIFIER")
    print("=" * 35)

    complaint = input("Enter customer complaint: ").strip()

    if not complaint:
        print("Please enter a customer complaint.")
        return

    try:
        result = classify_complaint(complaint)

        print("\nClassification:", result["classification"])
        print("Reason:", result["reason"])

    except json.JSONDecodeError:
        print("Error: The model returned invalid JSON.")

    except Exception as error:
        print(f"Classification failed: {error}")


if __name__ == "__main__":
    main()