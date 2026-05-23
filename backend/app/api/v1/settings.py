"""User settings, chatbot, and PDF reports."""
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.api.deps import get_current_user
from app.core.database import get_database
from app.schemas.energy import ChatMessage, SettingsUpdate
from app.services.ml_service import ml_service
from app.services.report_service import generate_pdf_report

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "full_name": user.get("full_name"),
        "preferred_language": user.get("preferred_language", "en"),
        "theme": user.get("theme", "dark"),
        "role": user.get("role", "user"),
    }


@router.patch("/profile")
async def update_profile(
    data: SettingsUpdate,
    user: dict = Depends(get_current_user),
):
    db = get_database()
    from bson import ObjectId

    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    if updates:
        await db.users.update_one({"_id": ObjectId(user["id"])}, {"$set": updates})
    return {"updated": True, **updates}


@router.post("/chat")
async def chat(data: ChatMessage, user: dict = Depends(get_current_user)):
    return ml_service.chatbot_reply(data.message, user["id"])


@router.get("/report/pdf")
async def download_report(user: dict = Depends(get_current_user)):
    path = generate_pdf_report(user["id"], user.get("full_name", "User"))
    return FileResponse(
        path,
        media_type="application/pdf",
        filename=path.split("/")[-1].split("\\")[-1],
    )


@router.get("/carbon-footprint")
async def carbon_footprint(user: dict = Depends(get_current_user)):
    from app.services.energy_simulator import get_simulator

    r = get_simulator(user["id"]).next_reading()
    trees_needed = r["carbon_kg"] / 21  # ~21 kg CO2 per tree per year
    return {
        "carbon_kg_monthly": r["carbon_kg"],
        "equivalent_trees": round(trees_needed, 1),
        "comparison": "vs. national avg household: -8% (simulated)",
    }
