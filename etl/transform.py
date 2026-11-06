import pandas as pd
import numpy as np
import logging
from sqlalchemy import create_engine
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database import DATABASE_URL

def load_raw_data_from_db():
    engine = create_engine(DATABASE_URL)
    matches_df = pd.read_sql_table("matches", con=engine)
    deliveries_df = pd.read_sql_table("deliveries", con=engine)
    return matches_df, deliveries_df

def assign_match_phase(over):
    if over < 6:
        return "Powerplay"
    elif over < 15:
        return "Middle"
    else:
        return "Death"

def transform_data(matches_df: pd.DataFrame, deliveries_df: pd.DataFrame):
    logging.info("Transforming matches and deliveries data...")
    
    # Ensure sorted order for cumulative statistics
    deliveries_df = deliveries_df.sort_values(by=["match_id", "inning", "over", "ball"]).reset_index(drop=True)
    
    # Assign match phase
    deliveries_df["match_phase"] = deliveries_df["over"].apply(assign_match_phase)
    
    # Binary wicket indicator
    deliveries_df["is_wicket"] = deliveries_df["player_dismissed"].notna().astype(int)
    
    # Extras breakdown
    deliveries_df["is_dot"] = (deliveries_df["runs_total"] == 0).astype(int)
    deliveries_df["is_boundary_four"] = (deliveries_df["runs_batter"] == 4).astype(int)
    deliveries_df["is_boundary_six"] = (deliveries_df["runs_batter"] == 6).astype(int)
    
    # Cumulative runs and wickets per match per inning
    deliveries_df["cumulative_runs"] = deliveries_df.groupby(["match_id", "inning"])["runs_total"].cumsum()
    deliveries_df["cumulative_wickets"] = deliveries_df.groupby(["match_id", "inning"])["is_wicket"].cumsum()
    
    # Current overs completed (approximate based on over number)
    deliveries_df["current_over_float"] = deliveries_df["over"] + (deliveries_df["ball"] / 6.0)
    deliveries_df["current_run_rate"] = np.where(
        deliveries_df["current_over_float"] > 0,
        (deliveries_df["cumulative_runs"] / deliveries_df["current_over_float"]).round(2),
        0.0
    )
    
    # Calculate Innings level aggregate
    innings_df = deliveries_df.groupby(["match_id", "inning"]).agg(
        total_runs=("runs_total", "sum"),
        total_wickets=("is_wicket", "sum"),
        total_overs=("over", "max"),
        total_balls=("ball", "count"),
        total_extras=("runs_extras", "sum"),
        total_fours=("is_boundary_four", "sum"),
        total_sixes=("is_boundary_six", "sum"),
        total_dots=("is_dot", "sum")
    ).reset_index()
    
    # Adjust total overs to include fractional over (e.g. 19.4)
    last_balls = deliveries_df.groupby(["match_id", "inning"]).last().reset_index()
    innings_df["final_over_str"] = last_balls["over"].astype(str) + "." + last_balls["ball"].astype(str)
    innings_df["run_rate"] = np.where(
        last_balls["current_over_float"] > 0,
        (innings_df["total_runs"] / last_balls["current_over_float"]).round(2),
        0.0
    )
    
    logging.info(f"Transformation complete. Deliveries: {len(deliveries_df)}, Innings: {len(innings_df)}")
    return matches_df, deliveries_df, innings_df

if __name__ == "__main__":
    m, d = load_raw_data_from_db()
    m_t, d_t, i_t = transform_data(m, d)
    print("Transformed sample:")
    print(d_t[["match_id", "inning", "over", "ball", "match_phase", "cumulative_runs", "cumulative_wickets"]].head())
