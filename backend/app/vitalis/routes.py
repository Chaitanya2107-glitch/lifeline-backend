from fastapi import APIRouter, Depends

from app.vitalis.schemas import ChatRequest, ChatResponse
from app.vitalis.service import generate_vitalis_response
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/vitalis",
    tags=["Vitalis AI Assistant"]
)


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):
    answer = generate_vitalis_response(
        current_user["user_id"],
        request.question
    )

    return {
        "answer": answer
    }
