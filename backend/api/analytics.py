from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from backend.dependencies import get_analytics_engine
from analytics.analytics_engine import AnalyticsEngine

router = APIRouter(prefix="/api/matches", tags=["Match Analytics"])

@router.get("/")
def get_matches(engine: AnalyticsEngine = Depends(get_analytics_engine)):
    return engine.match_service.get_all_matches()

@router.get("/{match_id}")
def get_match_details(match_id: str, engine: AnalyticsEngine = Depends(get_analytics_engine)):
    details = engine.match_service.get_match_details(match_id)
    if "error" in details.get("match_info", {}):
        raise HTTPException(status_code=404, detail=f"Match '{match_id}' not found")
    return details
