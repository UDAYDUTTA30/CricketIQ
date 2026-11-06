from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from backend.dependencies import get_analytics_engine
from analytics.analytics_engine import AnalyticsEngine

router = APIRouter(prefix="/api/teams", tags=["Teams"])

@router.get("/", response_model=List[str])
def get_teams(engine: AnalyticsEngine = Depends(get_analytics_engine)):
    return engine.team_service.get_all_teams()

@router.get("/h2h")
def get_head_to_head(
    team1: str = Query(...),
    team2: str = Query(...),
    engine: AnalyticsEngine = Depends(get_analytics_engine)
):
    return engine.team_service.get_head_to_head(team1, team2)

@router.get("/{name}")
def get_team_performance(name: str, engine: AnalyticsEngine = Depends(get_analytics_engine)):
    res = engine.team_service.get_performance(name)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res
