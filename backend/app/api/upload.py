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
    get_all_medical_records,
)
from fastapi import HTTPException
from app.ai.parser import AIResponseError
from fastapi import Depends
from app.auth.security import get_current_user

router = APIRouter()


@router.post("/upload")
async def upload_report(
    current_user=Depends(get_current_user),
    file: UploadFile = File(...)
):

    if file is None:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    allowed_extensions = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg"
    }

    suffix = Path(file.filename).suffix.lower()

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG and JPEG files are supported."
        )

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    try:

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # OCR
        text = extract_text(str(file_path))
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Unable to extract readable text from the uploaded report."
            )
        

        report_hash = generate_report_hash(text)

        existing_record = get_record_by_hash(
            current_user["user_id"],
            report_hash
        )

        if existing_record:
            return {
                "message": "Duplicate report detected.",
                "record": existing_record,
            }

        try:
            # AI
            ai_response = extract_medical_data(text)

        # Parse
            parsed = parse_ai_response(ai_response)

        # Validate
            record = validate_medical_record(parsed)
        except AIResponseError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid medical data extracted: {e}"
            )
        # Save to Supabase
        data = record.model_dump()

        data["report_hash"] = report_hash
        data["user_id"] = current_user["user_id"]

        saved_record = save_medical_record(data)

        return saved_record

    finally:
        if file_path.exists():
            file_path.unlink()



@router.get("/medical-records")
async def get_medical_records(
    current_user=Depends(get_current_user)
):
    return get_all_medical_records(
        current_user["user_id"]
    )
