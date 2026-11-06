import pandas as pd
from typing import Optional, List, Dict, Any

class FilterEngine:
    """Global filter engine for querying matches and deliveries data."""
    
    @staticmethod
    def filter_matches(
        matches_df: pd.DataFrame,
        venue: Optional[str] = None,
        teams: Optional[List[str]] = None,
        year: Optional[int] = None,
        winner: Optional[str] = None
    ) -> pd.DataFrame:
        df = matches_df.copy()
        
        if venue:
            df = df[df["venue"].str.contains(venue, case=False, na=False)]
            
        if teams:
            for team in teams:
                df = df[(df["team1"] == team) | (df["team2"] == team)]
                
        if year:
            df["year"] = pd.to_datetime(df["date"]).dt.year
            df = df[df["year"] == year]
            
        if winner:
            df = df[df["winner"] == winner]
            
        return df

    @staticmethod
    def filter_deliveries(
        deliveries_df: pd.DataFrame,
        match_ids: Optional[List[str]] = None,
        batter: Optional[str] = None,
        bowler: Optional[str] = None,
        match_phase: Optional[str] = None,
        inning: Optional[int] = None
    ) -> pd.DataFrame:
        df = deliveries_df.copy()
        
        if match_ids is not None:
            df = df[df["match_id"].isin(match_ids)]
            
        if batter:
            df = df[df["batter"] == batter]
            
        if bowler:
            df = df[df["bowler"] == bowler]
            
        if match_phase:
            df = df[df["match_phase"] == match_phase]
            
        if inning:
            df = df[df["inning"] == inning]
            
        return df
