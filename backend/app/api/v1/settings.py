from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.api.deps import get_current_user
from app.core.database import get_database
from app.schemas.auth import UserResponse
from app.schemas.energy import ChatMessage, ChatResponse, UserSettingsUpdate
from app.services.ml_service import chatbot_reply
from app.services.report_service import generate_monthly_pdf
from app.api.v1.energy import _build_snapshot
from bson import ObjectId

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.patch("", response_model=UserResponse)
async def update_settings(data: UserSettingsUpdate, user: dict = Depends(get_current_user)):
    db = get_database()
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if update:
        await db.users.update_one({"_id": ObjectId(user["id"])}, {"$set": update})
        user.update(update)
    return UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=user.get("role", "user"),
        language=user.get("language", "en"),
        theme=user.get("theme", "dark"),
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(data: ChatMessage, user: dict = Depends(get_current_user)):
    result = chatbot_reply(data.message)
    return ChatResponse(**result)


@router.get("/report/pdf")
async def download_report(user: dict = Depends(get_current_user)):
    snap = await _build_snapshot(user)
    pdf_bytes = generate_monthly_pdf(user, snap)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=energy_report.pdf"},
    )
