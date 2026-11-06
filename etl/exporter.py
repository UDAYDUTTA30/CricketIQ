import os
import pandas as pd
import logging

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INTERIM_DIR = os.path.join(BASE_DIR, "data", "interim")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
CACHE_DIR = os.path.join(BASE_DIR, "data", "cache")

def export_all(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
    innings_df: pd.DataFrame,
    batter_stats: pd.DataFrame,
    bowler_stats: pd.DataFrame,
    team_stats: pd.DataFrame,
    venue_stats: pd.DataFrame,
    score_pred_df: pd.DataFrame
):
    """Exports all transformed and aggregated data to CSV and Parquet files."""
    logging.info("Exporting data to CSV and Parquet files...")
    
    os.makedirs(INTERIM_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Export interim
    matches_df.to_csv(os.path.join(INTERIM_DIR, "matches.csv"), index=False)
    deliveries_df.to_csv(os.path.join(INTERIM_DIR, "deliveries.csv"), index=False)
    innings_df.to_csv(os.path.join(INTERIM_DIR, "innings.csv"), index=False)
    
    # Export processed
    batter_stats.to_csv(os.path.join(PROCESSED_DIR, "batter_stats.csv"), index=False)
    bowler_stats.to_csv(os.path.join(PROCESSED_DIR, "bowler_stats.csv"), index=False)
    team_stats.to_csv(os.path.join(PROCESSED_DIR, "team_stats.csv"), index=False)
    venue_stats.to_csv(os.path.join(PROCESSED_DIR, "venue_stats.csv"), index=False)
    score_pred_df.to_csv(os.path.join(PROCESSED_DIR, "score_prediction_dataset.csv"), index=False)
    
    # Export cache
    score_pred_df.to_parquet(os.path.join(CACHE_DIR, "feature_store.parquet"), index=False)
    batter_stats.to_parquet(os.path.join(CACHE_DIR, "player_cache.parquet"), index=False)
    venue_stats.to_parquet(os.path.join(CACHE_DIR, "venue_cache.parquet"), index=False)
    
    logging.info("Export completed successfully.")
