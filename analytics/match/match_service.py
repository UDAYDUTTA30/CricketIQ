import pandas as pd
from typing import Dict, Any, List
from analytics.match.worm_chart import get_worm_chart_data
from analytics.match.manhattan_chart import get_manhattan_chart_data
from analytics.match.partnerships import get_match_partnerships

class MatchService:
    def __init__(self, matches_df: pd.DataFrame, deliveries_df: pd.DataFrame):
        self.matches_df = matches_df
        self.deliveries_df = deliveries_df

    def get_all_matches(self) -> List[Dict[str, Any]]:
        return self.matches_df[["id", "team1", "team2", "venue", "date", "winner"]].fillna("").to_dict(orient="records")

    def get_match_details(self, match_id: str) -> Dict[str, Any]:
        match = self.matches_df[self.matches_df["id"] == match_id]
        if match.empty:
            return {"error": f"Match {match_id} not found"}
            
        match_info = match.fillna("").iloc[0].to_dict()
        worm = get_worm_chart_data(match_id, self.deliveries_df)
        manhattan = get_manhattan_chart_data(match_id, self.deliveries_df)
        partnerships = get_match_partnerships(match_id, self.deliveries_df)
        
        return {
            "match_info": match_info,
            "worm_chart": worm.get("worm_data"),
            "manhattan_chart": manhattan.get("manhattan_data"),
            "partnerships": partnerships.get("partnerships")
        }
