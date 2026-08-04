from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.database.supabase import supabase
from fastapi import Depends
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.get("/reports")
def get_reports(current_user=Depends(get_current_user)):

    reports = (
        supabase.table("reports")
        .select("*")
        .eq("user_id", current_user["user_id"])
        .execute()
    )

    return {
        "reports": reports.data
    }

@router.post("/")
async def upload_file(
    current_user=Depends(get_current_user),
    file: UploadFile = File(...)
):

    allowed_types = [
        "application/pdf",
        "image/jpeg",
        "image/png"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG and PNG files are allowed."
        )

    contents = await file.read()

    filename = f"{uuid4()}_{file.filename}"

    response = (
        supabase.storage
        .from_("medical-reports")
        .upload(
            path=filename,
            file=contents,
            file_options={
                "content-type": file.content_type
            }
        )
    )

    public_url = (
        supabase.storage
        .from_("medical-reports")
        .get_public_url(filename)
    )

    report = (
        supabase.table("reports")
        .insert({
            "user_id": current_user["user_id"],  # Temporary until we connect JWT
            "file_name": file.filename,
            "file_url": public_url,
            "file_type": file.content_type
        })
        .execute() )  

    return {
        "message": "File uploaded successfully",
        "report": report.data
    }
