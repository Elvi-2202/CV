import os
import httpx
import base64
import fitz 
from dotenv import load_dotenv 

load_dotenv() 

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_APP_NAME= os.getenv("OPENROUTER_APP_NAME", "cv")
OPENROUTER_SITE_URL=os.getenv("OPENROUTER_SITE_URL", "http://localhost/")

class OpenRouterError(RuntimeError):
    pass

def pdf_to_base64_image(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc.load_page(0)  
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) 
    img_bytes = pix.tobytes("jpeg")
    
    doc.close()
    return base64.b64encode(img_bytes).decode('utf-8')

async def analyze_pdf_cv(prompt: str, pdf_bytes: bytes) -> str: 
    if not OPENROUTER_API_KEY:
        raise OpenRouterError("OPENROUTER_API_KEY manquante")

    base64_image = pdf_to_base64_image(pdf_bytes)

    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Fais un resume  de ce CV en répondant à cette demande : {prompt}"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        
    if response.status_code >= 400:
        raise OpenRouterError(f"Erreur OpenRouter: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]