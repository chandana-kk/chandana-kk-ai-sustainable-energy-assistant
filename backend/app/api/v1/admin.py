from fastapi import APIRouter, Depends

from app.api.deps import get_admin_user, get_current_user
from app.core.database import get_database
from app.schemas.energy import AdminStats

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats", response_model=AdminStats)
async def admin_stats(admin: dict = Depends(get_admin_user)):
    db = get_database()
    total_users = await db.users.count_documents({})
    readings = await db.energy_readings.find().sort("recorded_at", -1).limit(100).to_list(100)
    total_kwh = sum(r.get("daily_kwh", 0) for r in readings)
    avg = total_kwh / len(readings) if readings else 0
    return AdminStats(
        total_users=total_users,
        active_sessions=max(1, total_users // 2),
        total_energy_kwh=round(total_kwh, 2),
        avg_daily_kwh=round(avg, 2),
        system_status="healthy",
    )


@router.post("/seed-admin")
async def seed_admin():
    """One-time helper to create admin user (development only)."""
    from datetime import datetime, timezone
    from app.core.security import hash_password
    db = get_database()
    email = "admin@smartenergy.ai"
    existing = await db.users.find_one({"email": email})
    if existing:
        return {"message": "Admin already exists", "email": email}
    await db.users.insert_one({
        "email": email,
        "full_name": "System Admin",
        "password_hash": hash_password("admin123"),
        "role": "admin",
        "language": "en",
        "theme": "dark",
        "created_at": datetime.now(timezone.utc),
    })
    return {"message": "Admin created", "email": email, "password": "admin123"}
