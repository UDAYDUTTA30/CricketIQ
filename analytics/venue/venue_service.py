import pandas as pd
from typing import Dict, Any, List
from analytics.venue.venue_analysis import get_venue_details

class VenueService:
    def __init__(self, matches_df: pd.DataFrame, deliveries_df: pd.DataFrame):
        self.matches_df = matches_df
        self.deliveries_df = deliveries_df

    def get_all_venues(self) -> List[str]:
        return sorted(self.matches_df["venue"].dropna().unique().tolist())

    def get_venue_profile(self, venue_name: str) -> Dict[str, Any]:
        return get_venue_details(venue_name, self.matches_df, self.deliveries_df)
