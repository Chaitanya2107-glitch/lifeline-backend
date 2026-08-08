from fastapi import APIRouter, Depends

from app.auth.security import get_current_user
from app.timeline.service import generate_timeline

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"]
)


@router.get("/")
def get_timeline(current_user=Depends(get_current_user)):
    return {
        "timeline": generate_timeline(current_user["user_id"])
    }
