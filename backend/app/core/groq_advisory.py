import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def generate_groq_advisory(code: str, language: str, context: str):
    """
    Calls Groq LLM and returns structured JSON:
    {
        "advisory": "...",
        "risk_modifier": int,
        "readiness_score": int
    }
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "advisory": "GROQ_API_KEY not configured.",
            "risk_modifier": 0,
            "readiness_score": 0
        }

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
You are a strict senior code reviewer.

Carefully analyze the following {language} code.
Only mention real issues that exist in the code.
Do not hallucinate.
Be specific and practical.

Return STRICTLY valid JSON in this format:

{{
  "advisory": "<Write 3-5 specific improvement suggestions based on the actual code>",
  "risk_modifier": <integer between 0 and 10>,
  "readiness_score": <integer between 0 and 100>
}}

Code:
{code}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return only valid JSON. No markdown. No explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # 🔹 Remove markdown JSON blocks if present
        content = re.sub(r"```json", "", content)
        content = re.sub(r"```", "", content).strip()

        # 🔹 Attempt JSON parsing
        try:
            parsed = json.loads(content)

            return {
                "advisory": parsed.get("advisory", ""),
                "risk_modifier": parsed.get("risk_modifier", 0),
                "readiness_score": parsed.get("readiness_score", 0)
            }

        except json.JSONDecodeError:
            # Fallback if malformed
            return {
                "advisory": content,
                "risk_modifier": 3,
                "readiness_score": 70
            }

    except Exception as e:
        return {
            "advisory": f"Groq error: {str(e)}",
            "risk_modifier": 0,
            "readiness_score": 0
        }
