import os
import re
from tavily import TavilyClient
from groq import Groq

def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def get_evidence(claim: str):
    tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    try:
        res = tavily.search(query=claim, search_depth="basic", max_results=3)
        results = res.get("results", [])
        evidence = []
        source = "N/A"

        if results:
            source = results[0].get("url", "N/A")
            for r in results:
                content = clean(r.get("content", ""))[:250]
                if content:
                    evidence.append(content)

        return " ".join(evidence)[:1000], source
    except Exception:
        return "", "N/A"

def verify_claim(claim: str) -> dict:
    groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    claim = clean(claim)
    evidence, source = get_evidence(claim)

    system_prompt = (
        "You are a fact checker. "
        "Classify the claim using the evidence. "
        "Reply with ONLY ONE WORD: VERIFIED, INACCURATE, or FALSE."
    )

    try:
        response = groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"CLAIM: {claim}\nEVIDENCE: {evidence}"}
            ],
            temperature=0
        )

        out = response.choices[0].message.content.upper()
        if "VERIFIED" in out:
            status = "Verified"
        elif "INACCURATE" in out:
            status = "Inaccurate"
        elif "FALSE" in out:
            status = "False"
        else:
            status = "Unknown"

        return {
            "Claim": claim,
            "Status": status,
            "Explanation": f"Classified as {status} based on web evidence.",
            "Source": source
        }
    except Exception as e:
        return {
            "Claim": claim,
            "Status": "Error",
            "Explanation": str(e),
            "Source": source
        }
