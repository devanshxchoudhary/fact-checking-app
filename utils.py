import pypdf
import re

def extract_text_from_pdf(uploaded_file) -> str:
    try:
        reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    except Exception:
        return ""
