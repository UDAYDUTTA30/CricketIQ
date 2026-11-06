import os
import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATASET_PATH = os.path.join(BASE_DIR, "data", "processed", "score_prediction_dataset.csv")

def load_and_split_dataset(test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}. Please run the ETL pipeline first.")
        
    df = pd.read_csv(DATASET_PATH)
    
    # Target variable
    y = df["final_score"]
    
    # Feature columns
    feature_cols = [
        "venue",
        "team1",
        "team2",
        "over",
        "ball",
        "current_over_float",
        "cumulative_runs",
        "cumulative_wickets",
        "current_run_rate",
        "runs_last_5_overs",
        "wickets_last_5_overs"
    ]
    X = df[feature_cols]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    return X_train, X_test, y_train, y_test
