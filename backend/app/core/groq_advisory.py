import os
from typing import Optional, Dict
from groq import Groq

def generate_groq_advisory(code: str, language: str, context: str) -> Optional[Dict]:

    api_key = os.getenv("GROQ_API_KEY")

    print("DEBUG: GROQ KEY PRESENT:", bool(api_key))

    if not api_key:
        print("DEBUG: No API key")
        return None

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",

            messages=[
                {"role": "system", "content": "You are an expert code reviewer."},
                {"role": "user", "content": code}
            ],
            temperature=0.2,
        )

        print("DEBUG: Groq response received")

        insight = response.choices[0].message.content

        return {
            "enabled": True,
            "provider": "Groq",
            "model": "llama3-8b-8192",
            "insight": insight,
            "disclaimer": "AI generated advisory."
        }

    except Exception as e:
        print("DEBUG: GROQ ERROR:", str(e))
        return None
