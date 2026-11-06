import pandas as pd
from typing import Dict, Any

def get_team_performance(team_name: str, matches_df: pd.DataFrame) -> Dict[str, Any]:
    played = matches_df[(matches_df["team1"] == team_name) | (matches_df["team2"] == team_name)]
    if played.empty:
        return {"error": f"Team {team_name} not found"}
        
    wins = len(matches_df[matches_df["winner"] == team_name])
    total = len(played)
    win_pct = round((wins / total * 100), 2) if total > 0 else 0.0
    
    by_venue = matches_df[matches_df["winner"] == team_name].groupby("venue")["id"].count().reset_index()
    by_venue.columns = ["venue", "wins"]
    
    return {
        "team": team_name,
        "total_matches": total,
        "wins": wins,
        "losses": total - wins,
        "win_percentage": win_pct,
        "wins_by_venue": by_venue.to_dict(orient="records")
    }
