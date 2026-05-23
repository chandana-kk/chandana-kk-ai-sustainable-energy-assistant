"""Admin panel APIs."""
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends

from app.api.deps import require_admin
from app.core.database import get_database
from app.core.security import hash_password

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/seed-admin")
async def seed_admin():
    """Create default admin (demo only)."""
    db = get_database()
    email = "admin@smartenergy.ai"
    if await db.users.find_one({"email": email}):
        return {"message": "Admin already exists", "email": email}
    result = await db.users.insert_one({
        "email": email,
        "password_hash": hash_password("admin123"),
        "full_name": "System Admin",
        "role": "admin",
        "preferred_language": "en",
        "theme": "dark",
        "created_at": datetime.now(timezone.utc),
    })
    return {"message": "Admin created", "email": email, "password": "admin123", "id": str(result.inserted_id)}


@router.get("/stats")
async def admin_stats(_: dict = Depends(require_admin)):
    db = get_database()
    user_count = await db.users.count_documents({})
    reading_count = await db.energy_readings.count_documents({})
    alert_count = await db.alerts.count_documents({})
    return {
        "users": user_count,
        "energy_readings": reading_count,
        "alerts": alert_count,
        "system_status": "healthy",
        "uptime": "simulated",
    }


@router.get("/users")
async def list_users(_: dict = Depends(require_admin)):
    db = get_database()
    users = []
    async for u in db.users.find({}, {"password_hash": 0}).limit(50):
        users.append({
            "id": str(u["_id"]),
            "email": u["email"],
            "full_name": u.get("full_name"),
            "role": u.get("role"),
            "created_at": u.get("created_at"),
        })
    return {"users": users}
