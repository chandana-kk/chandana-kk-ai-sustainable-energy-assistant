"""Authentication endpoints: register, login, forgot password."""
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.core.database import get_database
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.auth import ForgotPassword, TokenResponse, UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister):
    db = get_database()
    existing = await db.users.find_one({"email": data.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    doc = {
        "email": data.email.lower(),
        "password_hash": hash_password(data.password),
        "full_name": data.full_name,
        "role": "user",
        "preferred_language": data.preferred_language,
        "theme": "dark",
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.users.insert_one(doc)
    user_id = str(result.inserted_id)
    token = create_access_token(user_id)
    return TokenResponse(
        access_token=token,
        user={
            "id": user_id,
            "email": doc["email"],
            "full_name": doc["full_name"],
            "role": doc["role"],
            "preferred_language": doc["preferred_language"],
            "theme": doc["theme"],
        },
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    db = get_database()
    user = await db.users.find_one({"email": data.email.lower()})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    user_id = str(user["_id"])
    token = create_access_token(user_id)
    return TokenResponse(
        access_token=token,
        user={
            "id": user_id,
            "email": user["email"],
            "full_name": user.get("full_name", ""),
            "role": user.get("role", "user"),
            "preferred_language": user.get("preferred_language", "en"),
            "theme": user.get("theme", "dark"),
        },
    )


@router.post("/forgot-password")
async def forgot_password(data: ForgotPassword):
    db = get_database()
    user = await db.users.find_one({"email": data.email.lower()})
    if user:
        # Demo: log reset intent; production would send email
        await db.password_resets.insert_one({
            "user_id": str(user["_id"]),
            "email": data.email.lower(),
            "created_at": datetime.now(timezone.utc),
            "status": "pending",
        })
    return {
        "message": "If an account exists, password reset instructions have been sent.",
    }

