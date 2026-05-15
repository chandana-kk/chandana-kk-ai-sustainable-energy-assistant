from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.database import get_database
from app.schemas.energy import PredictionResponse
from app.services.ml_service import predict_energy
from datetime import datetime, timezone

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.get("/{horizon}", response_model=PredictionResponse)
async def get_predictions(horizon: str = "daily", user: dict = Depends(get_current_user)):
    if horizon not in ("daily", "weekly", "monthly"):
        horizon = "daily"
    result = predict_energy(horizon)
    db = get_database()
    await db.predictions.insert_one({
        "user_id": user["id"],
        **result,
        "created_at": datetime.now(timezone.utc),
    })
    return PredictionResponse(**result)
