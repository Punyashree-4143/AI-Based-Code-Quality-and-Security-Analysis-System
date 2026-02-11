import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def generate_groq_advisory(
    mode="single",
    code=None,
    project_summary=None,
    language="python",
    issues=None
):
    """
    Hybrid LLM advisory layer.
    Static remains authority.
    LLM gives architectural / quality suggestions only.
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

        # =========================================================
        # SINGLE FILE MODE
        # =========================================================
        if mode == "single":

            prompt = f"""
You are a strict senior code reviewer.

Analyze the following {language} code.

Only mention REAL issues present in the code.
Do NOT hallucinate.
Do NOT repeat obvious syntax errors.
Be concise and practical.

Return STRICTLY valid JSON only:

{{
  "advisory": "3-5 concrete improvement suggestions",
  "risk_modifier": 0-10,
  "readiness_score": 0-100
}}

Code:
{code}
"""

        # =========================================================
        # PROJECT MODE (Architectural Only)
        # =========================================================
        else:

            prompt = f"""
You are a senior software architect.

The static analyzer has already identified structural issues.

DO NOT repeat static issues.
Focus ONLY on:
- Architecture
- Modularity
- Maintainability
- Code organization
- Testing strategy

Project Summary:
{json.dumps(project_summary, indent=2)}

Return STRICTLY valid JSON:

{{
  "advisory": "Architectural and maintainability suggestions only",
  "risk_modifier": 0-5,
  "readiness_score": 0-100
}}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Return ONLY valid JSON. No markdown. No explanation."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # ---------------------------------------------------------
        # 🔒 SAFE JSON EXTRACTION (IGNORE EXTRA TEXT)
        # ---------------------------------------------------------
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if json_match:
            json_block = json_match.group(0)
            parsed = json.loads(json_block)
        else:
            raise ValueError("No valid JSON returned")

        # ---------------------------------------------------------
        # 🔒 SAFE INTEGER HANDLING
        # ---------------------------------------------------------
        try:
            risk_modifier = int(parsed.get("risk_modifier", 0))
        except:
            risk_modifier = 0

        try:
            readiness_score = int(parsed.get("readiness_score", 0))
        except:
            readiness_score = 0

        # Clamp values safely
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
