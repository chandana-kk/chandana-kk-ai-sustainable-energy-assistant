"""Seed demo user and sample data."""
import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow imports from backend
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / "backend" / ".env")
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.core.security import hash_password  # noqa: E402


async def seed():
    url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "smart_energy_ai")
    client = AsyncIOMotorClient(url)
    db = client[db_name]

    email = "demo@smartenergy.ai"
    existing = await db.users.find_one({"email": email})
    if not existing:
        await db.users.insert_one({
            "email": email,
            "password_hash": hash_password("demo123"),
            "full_name": "Demo User",
            "role": "user",
            "preferred_language": "en",
            "theme": "dark",
            "created_at": datetime.now(timezone.utc),
        })
        print(f"Created demo user: {email} / demo123")
    else:
        print(f"Demo user already exists: {email}")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
