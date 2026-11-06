import os
import pandas as pd

for path in ["data/interim/matches.csv", "data/interim/deliveries.csv", "data/processed/batter_stats.csv", "data/processed/bowler_stats.csv"]:
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"File: {path}")
        print(f"  Shape: {df.shape}")
        if "id" in df.columns:
            print(f"  Unique match IDs: {df['id'].nunique()}")
        if "match_id" in df.columns:
            print(f"  Unique match IDs: {df['match_id'].nunique()}")
        if "batter" in df.columns:
            print(f"  Unique batters: {df['batter'].nunique()}")
        if "player" in df.columns:
            print(f"  Unique players: {df['player'].nunique()}")
    else:
        print(f"File: {path} NOT FOUND")
