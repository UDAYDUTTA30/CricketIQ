from typing import List, Dict, Any
import pandas as pd
from analytics.player.batting_analysis import get_batter_summary
from analytics.player.bowling_analysis import get_bowler_summary

def compare_players(player1: str, player2: str, deliveries_df: pd.DataFrame) -> Dict[str, Any]:
    p1_bat = get_batter_summary(player1, deliveries_df)
    p2_bat = get_batter_summary(player2, deliveries_df)
    
    p1_bowl = get_bowler_summary(player1, deliveries_df)
    p2_bowl = get_bowler_summary(player2, deliveries_df)
    
    return {
        "player1": {
            "name": player1,
            "batting": p1_bat,
            "bowling": p1_bowl
        },
        "player2": {
            "name": player2,
            "batting": p2_bat,
            "bowling": p2_bowl
        }
    }
