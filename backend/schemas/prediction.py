from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class PredictionRequest(BaseModel):
    venue: str
    team1: str
    team2: str
    over: int
    ball: int
    cumulative_runs: int
    cumulative_wickets: int
    runs_last_5_overs: int
    wickets_last_5_overs: int
    model_name: Optional[str] = "random_forest"

    model_config = {"json_schema_extra": {
        "example": {
            "venue": "Melbourne Cricket Ground",
            "team1": "Australia",
            "team2": "Sri Lanka",
            "over": 10,
            "ball": 3,
            "cumulative_runs": 85,
            "cumulative_wickets": 2,
            "runs_last_5_overs": 42,
            "wickets_last_5_overs": 1,
            "model_name": "random_forest"
        }
    }}


class ConfidenceRange(BaseModel):
    low: int
    high: int


class PredictionResponse(BaseModel):
    model_used: str
    predicted_final_score: int
    confidence_range: ConfidenceRange
    current_state: Dict[str, Any]
    insights: List[str]


class SHAPContribution(BaseModel):
    feature: str
    shap_value: float


class SHAPExplanationResponse(BaseModel):
    model_name: str
    base_value: float
    top_feature_contributions: List[SHAPContribution]
