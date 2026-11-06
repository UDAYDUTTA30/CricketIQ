from fastapi import APIRouter, HTTPException
from backend.schemas.prediction import PredictionRequest, PredictionResponse, SHAPExplanationResponse
from ml.score_prediction.predict import predict_first_innings_score
from ml.score_prediction.explainability import get_shap_explanation

router = APIRouter(prefix="/api/prediction", tags=["AI Score Prediction"])

@router.post("/predict", response_model=PredictionResponse)
def predict_score(req: PredictionRequest):
    try:
        res = predict_first_innings_score(
            venue=req.venue,
            team1=req.team1,
            team2=req.team2,
            over=req.over,
            ball=req.ball,
            cumulative_runs=req.cumulative_runs,
            cumulative_wickets=req.cumulative_wickets,
            runs_last_5_overs=req.runs_last_5_overs,
            wickets_last_5_overs=req.wickets_last_5_overs,
            model_name=req.model_name or "random_forest"
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain", response_model=SHAPExplanationResponse)
def explain_prediction(req: PredictionRequest):
    try:
        sample_dict = {
            "venue": req.venue,
            "team1": req.team1,
            "team2": req.team2,
            "over": req.over,
            "ball": req.ball,
            "current_over_float": req.over + (req.ball / 6.0),
            "cumulative_runs": req.cumulative_runs,
            "cumulative_wickets": req.cumulative_wickets,
            "current_run_rate": round(req.cumulative_runs / (req.over + req.ball / 6.0), 2) if (req.over + req.ball / 6.0) > 0 else 0.0,
            "runs_last_5_overs": req.runs_last_5_overs,
            "wickets_last_5_overs": req.wickets_last_5_overs
        }
        res = get_shap_explanation(sample_dict, model_name=req.model_name or "random_forest")
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
