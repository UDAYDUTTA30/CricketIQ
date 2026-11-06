import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from etl.extract import parse_json_to_db
from etl.transform import load_raw_data_from_db, transform_data
from etl.validate import validate_raw_data
from etl.aggregate import (
    aggregate_batter_stats,
    aggregate_bowler_stats,
    aggregate_team_stats,
    aggregate_venue_stats
)
from etl.feature_engineering import build_score_prediction_dataset
from etl.exporter import export_all

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_etl_pipeline(limit=None):
    logging.info("Starting CricketIQ AI ETL Pipeline...")
    
    # 1. Extraction into SQLite
    parse_json_to_db(limit=limit)
    
    # 2. Load Raw Data from SQLite
    matches_df, deliveries_df = load_raw_data_from_db()
    
    # 3. Validation
    if not validate_raw_data(matches_df, deliveries_df):
        logging.error("ETL Pipeline aborted due to validation failure.")
        return
        
    # 4. Transformation
    matches_df, deliveries_df, innings_df = transform_data(matches_df, deliveries_df)
    
    # 5. Aggregations
    batter_stats = aggregate_batter_stats(deliveries_df)
    bowler_stats = aggregate_bowler_stats(deliveries_df)
    team_stats = aggregate_team_stats(matches_df, innings_df)
    venue_stats = aggregate_venue_stats(matches_df, innings_df)
    
    # 6. Feature Engineering
    score_pred_df = build_score_prediction_dataset(matches_df, deliveries_df, innings_df)
    
    # 7. Exporting to CSV and Parquet
    export_all(
        matches_df,
        deliveries_df,
        innings_df,
        batter_stats,
        bowler_stats,
        team_stats,
        venue_stats,
        score_pred_df
    )
    
    logging.info("ETL Pipeline execution completed successfully!")

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run_etl_pipeline(limit=limit)
