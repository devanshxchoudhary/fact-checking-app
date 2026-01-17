# ✅ AI Fact-Checking Web App

A production-ready web application that extracts factual claims from PDF documents and verifies them using live web data.

---

## 🚀 Features

- Upload a text-based PDF
- Extract up to 10 verifiable factual claims
- Verify claims using real-time web search
- Classify claims as:
  - Verified
  - Inaccurate
  - False
- Clean tabular output
- Free deployment on Streamlit Cloud

---

## 🧠 Architecture

PDF Upload
→ Text Extraction
→ Claim Extraction
→ Web Search
→ Claim Verification
→ Results Table

yaml
Copy code

No agents. Fully synchronous and deterministic.

---

## 🛠️ Tech Stack

- Python 3.10+
- Streamlit
- Groq LLM
- Tavily Search API
- pypdf

---

## 🔑 API Keys Required

- Groq API Key → https://console.groq.com
- Tavily API Key → https://tavily.com

---

## ▶️ Run Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Create secrets file:

bash
Copy code
mkdir -p .streamlit
nano .streamlit/secrets.toml
toml
Copy code
GROQ_API_KEY = "gsk_your_key_here"
TAVILY_API_KEY = "tvly_your_key_here"
Run app:

bash
Copy code
streamlit run app.py
