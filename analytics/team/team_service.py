import pandas as pd
from typing import Dict, Any, List
from analytics.team.head_to_head import get_head_to_head
from analytics.team.performance import get_team_performance


class TeamService:
    def __init__(self, matches_df: pd.DataFrame, deliveries_df: pd.DataFrame = None):
        self.matches_df = matches_df
        self.deliveries_df = deliveries_df

    def get_all_teams(self) -> List[str]:
        t1 = self.matches_df["team1"].dropna().unique()
        t2 = self.matches_df["team2"].dropna().unique()
        return sorted(list(set(t1).union(set(t2))))

    def get_performance(self, team_name: str) -> Dict[str, Any]:
        return get_team_performance(team_name, self.matches_df)

    def get_head_to_head(self, team1: str, team2: str) -> Dict[str, Any]:
        return get_head_to_head(team1, team2, self.matches_df, self.deliveries_df)
