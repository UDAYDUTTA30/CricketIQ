import os
import sys
import pandas as pd
from typing import Dict, Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from ml.score_prediction.model_registry import load_model

TYPICAL_T20_RR = 8.0  # baseline expected run rate in T20


def _safe_float(val) -> float:
    """Convert any numeric type to native Python float."""
    return float(val)

def _safe_int(val) -> int:
    return int(round(float(val)))


def predict_first_innings_score(
    venue: str,
    team1: str,
    team2: str,
    over: int,
    ball: int,
    cumulative_runs: int,
    cumulative_wickets: int,
    runs_last_5_overs: int,
    wickets_last_5_overs: int,
    model_name: str = "random_forest"
) -> Dict[str, Any]:
    model = load_model(model_name)

    current_over_float = over + (ball / 6.0)
    current_run_rate = round(cumulative_runs / current_over_float, 2) if current_over_float > 0 else 0.0
    overs_remaining = 20.0 - current_over_float
    wickets_remaining = 10 - cumulative_wickets

    input_data = pd.DataFrame([{
        "venue": venue,
        "team1": team1,
        "team2": team2,
        "over": over,
        "ball": ball,
        "current_over_float": current_over_float,
        "cumulative_runs": cumulative_runs,
        "cumulative_wickets": cumulative_wickets,
        "current_run_rate": current_run_rate,
        "runs_last_5_overs": runs_last_5_overs,
        "wickets_last_5_overs": wickets_last_5_overs
    }])

    prediction = model.predict(input_data)[0]
    predicted_score = _safe_int(prediction)
    projected_rr = round(_safe_float(predicted_score) / 20.0, 2)
    momentum_rr = round(runs_last_5_overs / 5.0, 2) if runs_last_5_overs > 0 else current_run_rate

    # Build plain-English insights
    insights: List[str] = []

    # Run rate context
    if current_run_rate >= TYPICAL_T20_RR + 2:
        insights.append(f"Excellent scoring rate of {current_run_rate:.1f} RPO — well above T20 par of {TYPICAL_T20_RR:.1f}.")
    elif current_run_rate >= TYPICAL_T20_RR:
        insights.append(f"On-par run rate of {current_run_rate:.1f} RPO at the {TYPICAL_T20_RR:.1f} T20 average.")
    else:
        insights.append(f"Below-par run rate of {current_run_rate:.1f} RPO — will need acceleration.")

    # Wickets context
    if cumulative_wickets == 0:
        insights.append("All 10 wickets in hand — ideal platform for a big finish.")
    elif cumulative_wickets <= 2:
        insights.append(f"Only {cumulative_wickets} wicket(s) lost — {wickets_remaining} wickets remaining gives strong runway.")
    elif cumulative_wickets <= 5:
        insights.append(f"{cumulative_wickets} wickets down with {wickets_remaining} remaining — mid-innings consolidation phase.")
    else:
        insights.append(f"Heavy fall of {cumulative_wickets} wickets — tail batting will limit scoring potential.")

    # Momentum context (last 5 overs)
    if over >= 5:
        if momentum_rr > current_run_rate + 1.5:
            insights.append(f"Strong recent momentum: {runs_last_5_overs} runs in last 5 overs ({momentum_rr:.1f} RPO) — accelerating.")
        elif momentum_rr < current_run_rate - 1.5:
            insights.append(f"Slowing momentum: only {runs_last_5_overs} runs in last 5 overs ({momentum_rr:.1f} RPO).")
        else:
            insights.append(f"Steady scoring in last 5 overs: {runs_last_5_overs} runs at {momentum_rr:.1f} RPO.")

    # Wickets fallen in last 5 overs
    if wickets_last_5_overs >= 3:
        insights.append(f"{wickets_last_5_overs} wickets in the last 5 overs — batting has been destabilised recently.")
    elif wickets_last_5_overs == 0 and over >= 5:
        insights.append("No wickets lost in the last 5 overs — solid batting partnership building momentum.")

    # Projected score context
    extras_remaining = overs_remaining * projected_rr
    insights.append(
        f"With {overs_remaining:.1f} overs remaining, the model projects {int(extras_remaining)} additional runs at {projected_rr:.1f} RPO."
    )

    return {
        "model_used": model_name,
        "predicted_final_score": predicted_score,
        "confidence_range": {
            "low": predicted_score - 12,
            "high": predicted_score + 12
        },
        "current_state": {
            "over": int(over),
            "ball": int(ball),
            "runs": int(cumulative_runs),
            "wickets": int(cumulative_wickets),
            "wickets_remaining": int(wickets_remaining),
            "current_rr": _safe_float(current_run_rate),
            "momentum_rr": _safe_float(momentum_rr),
            "projected_rr": _safe_float(projected_rr),
            "overs_remaining": round(_safe_float(overs_remaining), 1)
        },
        "insights": insights
    }
