import pandas as pd
import numpy as np
from typing import Dict, Any

def get_bowler_summary(bowler_name: str, deliveries_df: pd.DataFrame) -> Dict[str, Any]:
    b_df = deliveries_df[deliveries_df["bowler"] == bowler_name]
    if b_df.empty:
        return {"error": f"Bowler {bowler_name} not found"}
        
    conceded_df = b_df[~b_df["extras_type"].isin(["byes", "legbyes"])]
    conceded = int(conceded_df["runs_total"].sum())
    
    legal = b_df[~b_df["extras_type"].isin(["wides", "noballs"])]
    legal_balls = len(legal)
    
    wicket_kinds = ["bowled", "caught", "lbw", "stumped", "caught and bowled", "hit wicket"]
    wickets = int(b_df[b_df["dismissal_kind"].isin(wicket_kinds)]["is_wicket"].sum())
    
    overs = (legal_balls // 6) + (legal_balls % 6) / 10.0
    overs_dec = legal_balls / 6.0
    
    economy = round((conceded / overs_dec), 2) if overs_dec > 0 else 0.0
    avg = round((conceded / wickets), 2) if wickets > 0 else 0.0
    sr = round((legal_balls / wickets), 2) if wickets > 0 else 0.0
    dots = int((legal["runs_total"] == 0).sum())
    
    # Phase breakdown
    phase_stats = b_df.groupby("match_phase").agg(
        conceded=("runs_total", "sum"),
        wickets=("is_wicket", "sum"),
        balls=("ball", "count")
    ).reset_index()
    
    return {
        "bowler": bowler_name,
        "innings": b_df["match_id"].nunique(),
        "conceded": conceded,
        "legal_balls": legal_balls,
        "overs": overs,
        "wickets": wickets,
        "economy": economy,
        "average": avg,
        "strike_rate": sr,
        "dots": dots,
        "phase_breakdown": phase_stats.to_dict(orient="records")
    }
