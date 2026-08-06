from fastapi import APIRouter

from app.timeline.service import generate_timeline

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"]
)


@router.get("/")
def get_timeline():

    return {
        "timeline": generate_timeline()
    }
