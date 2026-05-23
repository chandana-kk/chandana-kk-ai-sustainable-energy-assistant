"""Optimization recommendation engine API."""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.services.ml_service import ml_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("")
async def get_recommendations(user: dict = Depends(get_current_user)):
    return {"recommendations": ml_service.get_recommendations(user["id"])}


@router.get("/nilm")
async def nilm_breakdown(user: dict = Depends(get_current_user)):
    return ml_service.nilm_breakdown(user["id"])
