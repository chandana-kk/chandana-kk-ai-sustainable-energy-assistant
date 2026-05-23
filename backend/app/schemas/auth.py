"""Authentication request/response schemas."""
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=2, max_length=100)
    preferred_language: Literal["en", "kn", "hi", "ta", "te"] = "en"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ForgotPassword(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserProfile(BaseModel):
    id: str
    email: str
    full_name: str
    role: str = "user"
    preferred_language: str = "en"
    theme: str = "dark"
