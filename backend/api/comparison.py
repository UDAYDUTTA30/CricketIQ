from fastapi import APIRouter, Depends, HTTPException, Query
from backend.dependencies import get_analytics_engine
from analytics.analytics_engine import AnalyticsEngine

router = APIRouter(prefix="/api/comparison", tags=["Player & Team Comparison"])

@router.get("/players")
def compare_players(
    player1: str = Query(...),
    player2: str = Query(...),
    engine: AnalyticsEngine = Depends(get_analytics_engine)
):
    return engine.player_service.compare(player1, player2)
