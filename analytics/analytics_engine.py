import os
import pandas as pd
import logging
from analytics.player.player_service import PlayerService
from analytics.team.team_service import TeamService
from analytics.venue.venue_service import VenueService
from analytics.match.match_service import MatchService

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INTERIM_DIR = os.path.join(BASE_DIR, "data", "interim")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

class AnalyticsEngine:
    def __init__(self):
        logging.info("Initializing AnalyticsEngine...")
        
        matches_path = os.path.join(INTERIM_DIR, "matches.csv")
        deliveries_path = os.path.join(INTERIM_DIR, "deliveries.csv")
        batter_stats_path = os.path.join(PROCESSED_DIR, "batter_stats.csv")
        bowler_stats_path = os.path.join(PROCESSED_DIR, "bowler_stats.csv")
        
        if os.path.exists(matches_path) and os.path.exists(deliveries_path):
            self.matches_df = pd.read_csv(matches_path)
            self.deliveries_df = pd.read_csv(deliveries_path)
        else:
            logging.warning("Data files not found in interim/processed dirs. Initializing empty engine.")
            self.matches_df = pd.DataFrame()
            self.deliveries_df = pd.DataFrame()
            
        self.player_service = PlayerService(self.deliveries_df)
        self.team_service = TeamService(self.matches_df, self.deliveries_df)
        self.venue_service = VenueService(self.matches_df, self.deliveries_df)
        self.match_service = MatchService(self.matches_df, self.deliveries_df)

    def reload(self):
        """Reloads datasets from disk."""
        self.__init__()
