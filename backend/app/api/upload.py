from fastapi import APIRouter, File, UploadFile
import shutil
from pathlib import Path

from app.ai.ocr_manager import extract_text
from app.ai.ai_manager import extract_medical_data
from app.ai.parser import parse_ai_response
from app.ai.validator import validate_medical_record
from app.services.medical_record_service import save_medical_record
from app.utils.hash import generate_report_hash
from app.services.medical_record_service import (
    save_medical_record,
    get_record_by_hash,
)
from app.services.medical_record_service import (
    save_medical_record,
    get_record_by_hash,
    get_all_medical_records,
)

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

        report_hash = generate_report_hash(text)

        existing_record = get_record_by_hash(report_hash)

        if existing_record:
            return {
                "message": "Duplicate report detected.",
                "record": existing_record,
            }

        

        # AI
        ai_response = extract_medical_data(text)

        # Parse
        parsed = parse_ai_response(ai_response)

        # Validate
        record = validate_medical_record(parsed)

        # Save to Supabase
        
        data = record.model_dump()
        data["report_hash"] = report_hash

        saved_record = save_medical_record(data)

        return saved_record

    finally:
        if file_path.exists():
            file_path.unlink()

@router.get("/medical-records")
async def get_medical_records():
    return get_all_medical_records()
