from fastapi import APIRouter, HTTPException

from app.auth.schemas import RegisterRequest
from app.auth.security import hash_password
from app.database.supabase import supabase
from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.security import verify_password, create_access_token
from fastapi import Depends
from app.auth.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: RegisterRequest):

    # Check if email already exists
    existing = (
        supabase.table("users")
        .select("*")
        .eq("email", user.email)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Insert user
    result = (
        supabase.table("users")
        .insert({
            "email": user.email,
            "password_hash": hash_password(user.password),
            "name": user.name
        })
        .execute()
    )

    return {
        "message": "User registered successfully",
        "user": result.data
    }


@router.post("/login", response_model=TokenResponse)
def login(user: LoginRequest):

    # Find user by email
    result = (
        supabase.table("users")
        .select("*")
        .eq("email", user.email)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    db_user = result.data[0]

    # Verify password
    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT
    token = create_access_token(
        {
            "sub": db_user["email"],
            "user_id": db_user["id"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "message": "Authenticated successfully",
        "user": current_user
    }
