from fastapi import APIRouter, File, UploadFile
import shutil
from pathlib import Path

from app.ai.ocr_manager import extract_text
from app.ai.ai_manager import extract_medical_data
from app.ai.parser import parse_ai_response
from app.ai.validator import validate_medical_record
from app.services.medical_record_service import save_medical_record

router = APIRouter()


@router.post("/upload")
async def upload_report(file: UploadFile = File(...)):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # OCR
        text = extract_text(str(file_path))

        # AI
        ai_response = extract_medical_data(text)

        # Parse
        parsed = parse_ai_response(ai_response)

        # Validate
        record = validate_medical_record(parsed)

        # Save to Supabase
        saved_record = save_medical_record(record.model_dump())

        return saved_record

    finally:
        if file_path.exists():
            file_path.unlink()
