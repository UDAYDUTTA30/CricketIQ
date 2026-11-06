from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from backend.dependencies import get_analytics_engine
from analytics.analytics_engine import AnalyticsEngine

router = APIRouter(prefix="/api/venues", tags=["Venues"])

@router.get("/", response_model=List[str])
def get_venues(engine: AnalyticsEngine = Depends(get_analytics_engine)):
    return engine.venue_service.get_all_venues()

@router.get("/{name}")
def get_venue_profile(name: str, engine: AnalyticsEngine = Depends(get_analytics_engine)):
    profile = engine.venue_service.get_venue_profile(name)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile
