import pandas as pd
from typing import Dict, Any

def get_venue_details(venue_name: str, matches_df: pd.DataFrame, deliveries_df: pd.DataFrame) -> Dict[str, Any]:
    v_matches = matches_df[matches_df["venue"] == venue_name]
    if v_matches.empty:
        return {"error": f"Venue {venue_name} not found"}
        
    match_ids = v_matches["id"].tolist()
    v_deliv = deliveries_df[deliveries_df["match_id"].isin(match_ids)]
    
    first_inn_runs = v_deliv[v_deliv["inning"] == 1].groupby("match_id")["runs_total"].sum()
    second_inn_runs = v_deliv[v_deliv["inning"] == 2].groupby("match_id")["runs_total"].sum()
    
    return {
        "venue": venue_name,
        "total_matches": len(v_matches),
        "avg_1st_inn_score": round(first_inn_runs.mean(), 2) if len(first_inn_runs) > 0 else 0.0,
        "avg_2nd_inn_score": round(second_inn_runs.mean(), 2) if len(second_inn_runs) > 0 else 0.0,
        "highest_score": int(first_inn_runs.max()) if len(first_inn_runs) > 0 else 0,
        "lowest_score": int(first_inn_runs.min()) if len(first_inn_runs) > 0 else 0
    }
