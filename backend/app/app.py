from fastapi import FastAPI, Request, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse as FastAPIFileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from app.schemas import FileResponse
import shutil
import uuid
from app.text_extracting import extract_text
from app.LLM_Integration import generate_notes
from app.database import initialize_database, get_notes_by_file_id, save_notes, save_file



app = FastAPI()

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port and common React port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A simple root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# This is so the user can upload their file (CREATE)
@app.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4()) + "_" + file.filename
        file_location = os.path.join(UPLOAD_DIR, file_id)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        # Save file metadata to database
        save_file(file_id, file.filename)
        return {"file_id": file_id, "filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    


# Endpoint to get their file (READ)
@app.get("/file/{file_id}")
async def get_file(file_id: str):
    path = os.path.join(UPLOAD_DIR, file_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FastAPIFileResponse(path, filename=file_id)


# Endpoint to update their file (UPDATE)
@app.put("/file/{file_id}", response_model=FileResponse)
async def update_file(file_id: str, file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file_id)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "message": "File updated successfully"
    }


# Endpoint to delete their file (DELETE)
@app.delete("/file/{file_id}")
async def delete_file(file_id: str):
    path = os.path.join(UPLOAD_DIR, file_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(path)
    return {"message": f"File {file_id} deleted successfully"}


# Notes Endpoint
@app.post("/notes/{file_id}")
async def generate_notes_endpoint(file_id: str):
    import traceback
    import logging
    
    logger = logging.getLogger(__name__)
    
    path = os.path.join(UPLOAD_DIR, file_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        print(f"[DEBUG] Checking cache for file_id: {file_id}")
        existing_notes = get_notes_by_file_id(file_id)
        if existing_notes:
            print(f"[DEBUG] Found cached notes")
            return {
                "file_id": file_id,
                "notes": existing_notes,
                "cached": True
            }

        print(f"[DEBUG] Extracting text from file: {file_id}")
        with open(path, "rb") as f:
            text = extract_text(f, file_id)
        print(f"[DEBUG] Extracted text length: {len(text)} characters")

        print(f"[DEBUG] Generating notes via LLM...")
        notes = generate_notes(text)
        print(f"[DEBUG] Notes generated successfully, length: {len(notes)}")
        
        print(f"[DEBUG] Saving notes to database...")
        save_notes(
            file_id=file_id,
            content=notes,
            model="llama3"
        )
        print(f"[DEBUG] Notes saved successfully")
        
        return {
            "file_id": file_id,
            "notes": notes,
            "cached": False
        }

    except ValueError as ve:
        print(f"[ERROR] ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        error_msg = str(re)
        print(f"[ERROR] RuntimeError: {error_msg}")
        print(traceback.format_exc())
        if "Ollama request failed" in error_msg:
            raise HTTPException(
                status_code=503,
                detail=f"Ollama service error: {error_msg}. Make sure Ollama is running at http://localhost:11434"
            )
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_detail = str(e)
        error_trace = traceback.format_exc()
        print(f"[ERROR] Unexpected error: {error_detail}")
        print(f"[ERROR] Traceback:\n{error_trace}")
        logger.error(f"Error generating notes: {error_detail}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating notes: {error_detail}"
        )
    


# Initialize the database when the application starts
@app.on_event("startup")
def on_startup():
    initialize_database()