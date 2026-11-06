from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from backend.dependencies import get_analytics_engine
from analytics.analytics_engine import AnalyticsEngine

router = APIRouter(prefix="/api/players", tags=["Players"])

@router.get("/", response_model=List[str])
def get_players(engine: AnalyticsEngine = Depends(get_analytics_engine)):
    return engine.player_service.get_all_players()

@router.get("/{name}")
def get_player_profile(name: str, engine: AnalyticsEngine = Depends(get_analytics_engine)):
    profile = engine.player_service.get_player_profile(name)
    if "error" in profile.get("batting", {}) and "error" in profile.get("bowling", {}):
        raise HTTPException(status_code=404, detail=f"Player '{name}' not found")
    return profile
