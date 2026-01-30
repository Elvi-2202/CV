from fastapi import FastAPI, UploadFile, File
import uuid
from app.routers import ai


app = FastAPI()

app.include_router(ai.router)

def generated_uuid():
    return str(uuid.uuid4())

MAX_FILE_SIZE= 5*1024*1024

@app.get("/ping")
def read_ping():
    return {"message": "pong"}

# @app.post("/cvs/upload")
# async def upload_cv(file: UploadFile):
#     if file.content_type != "application/pdf":
#         return {"error": "Unsupported media type", "status_code": 415}
    
#     if file.size > MAX_FILE_SIZE:
#         return {"error": "Payload too large", "status_code": 413}
    
#     cv_id = generated_uuid()
#     file_path = f"upload/cvs/{cv_id}.pdf"
#     save_file_bytes(file_path, file.content)

#     return {
#         "id": cv_id
#         "filename": file.filename
#     }
@app.post("/cvs/upload")
async def upload_cv(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"error": "Unsupported media type", "status_code": 415}
    if file.size > MAX_FILE_SIZE:
        return {"error": "Payload too large", "status_code": 413}
    
    cv_id = generated_uuid()
    file_path = f"upload/cvs/{cv_id}.pdf"
    
    content = await file.read() 
    return {"size_of_file": len(content), "name_file": file.filename, "id": cv_id, "filename": file.filename }   
   
