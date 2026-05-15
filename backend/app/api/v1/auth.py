from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.database import get_database
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.schemas.auth import ForgotPassword, TokenResponse, UserLogin, UserRegister, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister):
    db = get_database()
    existing = await db.users.find_one({"email": data.email.lower()})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    doc = {
        "email": data.email.lower(),
        "full_name": data.full_name,
        "password_hash": hash_password(data.password),
        "role": "user",
        "language": "en",
        "theme": "dark",
        "bill_threshold": 5000.0,
        "notifications_enabled": True,
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.users.insert_one(doc)
    user_id = str(result.inserted_id)
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    db = get_database()
    user = await db.users.find_one({"email": data.email.lower()})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user_id = str(user["_id"])
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/forgot-password")
async def forgot_password(data: ForgotPassword):
    db = get_database()
    user = await db.users.find_one({"email": data.email.lower()})
    if user:
        await db.password_resets.insert_one({
            "user_id": user["_id"],
            "email": data.email.lower(),
            "created_at": datetime.now(timezone.utc),
            "status": "pending",
        })
    return {"message": "If the email exists, reset instructions have been sent."}


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: dict):
    token = body.get("refresh_token", "")
    payload = decode_token(token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = payload.get("sub")
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user: dict = Depends(get_current_user)):
    return UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=user.get("role", "user"),
        language=user.get("language", "en"),
        theme=user.get("theme", "dark"),
    )
