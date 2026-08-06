from fastapi import APIRouter, Depends

from app.summary.service import generate_summary
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/summary",
    tags=["Doctor Summary"]
)


@router.get("/")
def get_summary(
    current_user=Depends(get_current_user),
):
    return {
        "summary": generate_summary(
            current_user["user_id"]
        )
    }
