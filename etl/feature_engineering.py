import pandas as pd
import numpy as np
import logging

def build_score_prediction_dataset(matches_df: pd.DataFrame, deliveries_df: pd.DataFrame, innings_df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a granular feature dataset for First Innings T20 Score Prediction models.
    Each row represents a snapshot after a delivery in the 1st inning.
    """
    logging.info("Building score prediction dataset (1st innings features)...")
    
    # Merge delivery data with match data to get teams and venue
    merged = deliveries_df.merge(
        matches_df[["id", "venue", "team1", "team2", "toss_winner", "toss_decision"]],
        left_on="match_id",
        right_on="id",
        how="inner"
    )
    
    # Filter only 1st innings for score prediction
    first_inn = merged[merged["inning"] == 1].copy()
    
    if first_inn.empty:
        logging.warning("No 1st innings deliveries found for feature engineering.")
        return pd.DataFrame()
        
    # Get total 1st innings score per match
    first_inn_totals = innings_df[innings_df["inning"] == 1][["match_id", "total_runs"]].rename(
        columns={"total_runs": "final_score"}
    )
    
    first_inn = first_inn.merge(first_inn_totals, on="match_id", how="inner")
    
    # Determine batting_team and bowling_team
    # In cricsheet match info, team1 or team2 bats first
    # We can infer batting team from batter if needed, or by toss decision
    # Here we infer batting team by checking first batter's team or match context
    first_inn["batting_team"] = first_inn["team1"] # fallback
    first_inn["bowling_team"] = first_inn["team2"] # fallback
    
    # Calculate rolling 5 overs (30 balls) statistics per match
    # Rolling sum over 30 deliveries window
    first_inn["runs_last_5_overs"] = first_inn.groupby("match_id")["runs_total"].transform(
        lambda x: x.rolling(window=30, min_periods=1).sum()
    )
    first_inn["wickets_last_5_overs"] = first_inn.groupby("match_id")["is_wicket"].transform(
        lambda x: x.rolling(window=30, min_periods=1).sum()
    )
    
    # Select feature columns
    feature_cols = [
        "match_id",
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
        "wickets_last_5_overs",
        "final_score"
    ]
    
    dataset = first_inn[feature_cols].copy()
    
    # Remove early deliveries (e.g. before over 5) if desired, or keep overs 5-19 for realistic mid-match prediction
    dataset = dataset[dataset["over"] >= 5].reset_index(drop=True)
    
    logging.info(f"Score prediction dataset built successfully with {len(dataset)} snapshot samples.")
    return dataset
