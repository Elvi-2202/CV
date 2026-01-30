from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.openrouter_client import analyze_pdf_cv

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/cv") 
async def ai_analyze(
    prompt: str = Form("Peux tu me resumer les competences et les experiences de ce candidat ?"), 
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="L'API n'accepte que les fichiers PDF.")

    pdf_bytes = await file.read()
    
    try:
        answer = await analyze_pdf_cv(prompt, pdf_bytes)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))