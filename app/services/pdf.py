import pdfplumber
import pdf

def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) :
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            text += page_text + "\n"
        return text.strip()