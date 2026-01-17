import os
import re
from groq import Groq

def fallback_claims(text: str):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    claims = []
    for s in sentences:
        if re.search(r'\$|\d+%|\d{4}|\d+\.\d+|\d+', s):
            s = re.sub(r'\s+', ' ', s).strip()
            if len(s) > 25:
                claims.append(s)
        if len(claims) >= 10:
            break
    return claims

def extract_claims(text: str) -> list:
    if not text:
        return []

    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        prompt = (
            "Extract up to 10 factual, verifiable claims from the text. "
            "Claims must contain numbers, dates, or statistics. "
            "Return each claim on a new line. Do not format as JSON."
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text[:12000]}
            ],
            temperature=0
        )

        lines = response.choices[0].message.content.split("\n")
        claims = [re.sub(r'^[-*\d.]+', '', l).strip() for l in lines if len(l.strip()) > 20]

        if claims:
            return claims[:10]
    except Exception:
        pass

    return fallback_claims(text)
