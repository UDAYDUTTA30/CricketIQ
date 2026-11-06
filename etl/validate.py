import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def validate_raw_data(matches_df: pd.DataFrame, deliveries_df: pd.DataFrame) -> bool:
    """Validates the extracted matches and deliveries DataFrames."""
    logging.info("Validating extracted data...")
    
    if matches_df.empty:
        logging.error("Matches DataFrame is empty!")
        return False
        
    if deliveries_df.empty:
        logging.error("Deliveries DataFrame is empty!")
        return False
        
    # Required columns check
    required_match_cols = ["id", "team1", "team2", "venue", "date"]
    for col in required_match_cols:
        if col not in matches_df.columns:
            logging.error(f"Missing column in matches_df: {col}")
            return False
            
    required_delivery_cols = ["match_id", "inning", "over", "ball", "batter", "bowler", "runs_total"]
    for col in required_delivery_cols:
        if col not in deliveries_df.columns:
            logging.error(f"Missing column in deliveries_df: {col}")
            return False

    # Check non-negative runs
    if (deliveries_df["runs_total"] < 0).any():
        logging.warning("Found negative runs in deliveries_df!")
        
    logging.info("Data validation passed successfully.")
    return True
