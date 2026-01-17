import streamlit as st
import os
import pandas as pd
from utils import extract_text_from_pdf
from claim_extractor import extract_claims
from verifier import verify_claim

st.set_page_config(page_title="AI Fact Checker", page_icon="✅", layout="wide")

try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    if "TAVILY_API_KEY" in st.secrets:
        os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
except FileNotFoundError:
    pass

st.title("✅ AI Fact-Checking Web App")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded and os.environ.get("GROQ_API_KEY") and os.environ.get("TAVILY_API_KEY"):
    if st.button("Analyze & Verify"):
        with st.spinner("Processing..."):
            text = extract_text_from_pdf(uploaded)
            claims = extract_claims(text)
            results = [verify_claim(c) for c in claims]

            if results:
                st.dataframe(pd.DataFrame(results), use_container_width=True)
            else:
                st.warning("No verifiable claims found.")
else:
    st.info("Upload PDF and configure API keys.")
