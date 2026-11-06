from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class TeamPerformanceResponse(BaseModel):
    team: str
    total_matches: int
    wins: int
    losses: int
    win_percentage: float
    wins_by_venue: List[Dict[str, Any]]

class VenueProfileResponse(BaseModel):
    venue: str
    total_matches: int
    avg_1st_inn_score: float
    avg_2nd_inn_score: float
    highest_score: int
    lowest_score: int
