import os
import json
import re
from groq import Groq


def generate_groq_advisory(
    mode="single",
    code=None,
    project_summary=None,
    language="python",
    issues=None
):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or not api_key.strip():
        return {
            "advisory": "GROQ_API_KEY not configured.",
            "risk_modifier": 0,
            "readiness_score": 0
        }

    try:
        client = Groq(api_key=api_key.strip())

        # ===============================
        # Build Prompt
        # ===============================

        if mode == "single":
            prompt = f"""
You are a strict senior code reviewer.

Analyze this {language} code.
Only mention REAL issues.
Return ONLY valid JSON:

{{
  "advisory": "3-5 improvement suggestions",
  "risk_modifier": 0-10,
  "readiness_score": 0-100
}}

Code:
{code}
"""
        else:
            prompt = f"""
You are a senior software architect.

Analyze this project summary.
Focus on architecture and maintainability only.

Project Summary:
{json.dumps(project_summary, indent=2)}

Return ONLY valid JSON:

{{
  "advisory": "Architectural improvements",
  "risk_modifier": 0-5,
  "readiness_score": 0-100
}}
"""

        # ===============================
        # Call Groq
        # ===============================

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return strictly JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        # 🔒 SAFE RESPONSE CHECK
        if not response or not response.choices:
            raise ValueError("Empty response from Groq")

        content = response.choices[0].message.content

        if not content or not content.strip():
            raise ValueError("Groq returned empty content")

        content = content.strip()

        # 🔒 Extract first JSON block safely (non-greedy)
        json_match = re.search(r"\{.*?\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in Groq response")

        json_block = json_match.group(0)

        parsed = json.loads(json_block)

        # 🔒 Safe int conversion
        try:
            risk_modifier = int(parsed.get("risk_modifier", 0))
        except:
            risk_modifier = 0

        try:
            readiness_score = int(parsed.get("readiness_score", 0))
        except:
            readiness_score = 0

        # Clamp safely
        if mode == "project":
            risk_modifier = max(0, min(risk_modifier, 5))
        else:
            risk_modifier = max(0, min(risk_modifier, 10))

        readiness_score = max(0, min(readiness_score, 100))

        return {
            "advisory": parsed.get("advisory", ""),
            "risk_modifier": risk_modifier,
            "readiness_score": readiness_score
        }

    except Exception as e:
        return {
            "advisory": f"Groq error: {str(e)}",
            "risk_modifier": 0,
            "readiness_score": 0
        }
