import pandas as pd
from typing import Dict, Any, List
from analytics.player.batting_analysis import get_batter_summary
from analytics.player.bowling_analysis import get_bowler_summary
from analytics.player.comparison import compare_players

class PlayerService:
    def __init__(self, deliveries_df: pd.DataFrame, batter_stats_df: pd.DataFrame = None, bowler_stats_df: pd.DataFrame = None):
        self.deliveries_df = deliveries_df
        self.batter_stats_df = batter_stats_df
        self.bowler_stats_df = bowler_stats_df

    def get_all_players(self) -> List[str]:
        batters = self.deliveries_df["batter"].dropna().unique()
        bowlers = self.deliveries_df["bowler"].dropna().unique()
        return sorted(list(set(batters).union(set(bowlers))))

    def get_player_profile(self, player_name: str) -> Dict[str, Any]:
        batting = get_batter_summary(player_name, self.deliveries_df)
        bowling = get_bowler_summary(player_name, self.deliveries_df)
        return {
            "name": player_name,
            "batting": batting,
            "bowling": bowling
        }

    def compare(self, player1: str, player2: str) -> Dict[str, Any]:
        return compare_players(player1, player2, self.deliveries_df)
