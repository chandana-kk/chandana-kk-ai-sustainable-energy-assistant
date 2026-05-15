"""Seed admin user and sample data. Run from project root with MongoDB running."""

import asyncio
from datetime import datetime, timezone
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
from app.core.security import hash_password


async def seed():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.mongodb_db_name]
    email = "demo@smartenergy.ai"
    if not await db.users.find_one({"email": email}):
        await db.users.insert_one({
            "email": email,
            "full_name": "Demo User",
            "password_hash": hash_password("demo123"),
            "role": "user",
            "language": "en",
            "theme": "dark",
            "bill_threshold": 5000.0,
            "created_at": datetime.now(timezone.utc),
        })
        print(f"Created demo user: {email} / demo123")
    else:
        print("Demo user already exists")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
