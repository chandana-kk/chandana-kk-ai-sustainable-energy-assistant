from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.database import get_database
from app.schemas.energy import Recommendation
from app.services.ml_service import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=list[Recommendation])
async def get_recommendations(user: dict = Depends(get_current_user)):
    recs = generate_recommendations(user)
    db = get_database()
    await db.recommendations.insert_one({
        "user_id": user["id"],
        "items": recs,
        "created_at": datetime.now(timezone.utc),
    })
    return [Recommendation(**r) for r in recs]
