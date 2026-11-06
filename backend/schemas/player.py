from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class PlayerProfileResponse(BaseModel):
    name: str
    batting: Dict[str, Any]
    bowling: Dict[str, Any]

class PlayerComparisonRequest(BaseModel):
    player1: str
    player2: str
