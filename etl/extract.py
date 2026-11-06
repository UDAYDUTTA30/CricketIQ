import os
import json
import glob
import sys
import time
import pandas as pd
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database import DATABASE_URL

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "cricsheet_json")

def parse_json_to_db(limit=None):
    engine = create_engine(DATABASE_URL)
    files = glob.glob(os.path.join(RAW_DATA_DIR, "*.json"))
    
    if limit:
        files = files[:limit]
        
    print(f"Found {len(files)} JSON files. Starting fast extraction...")
    t0 = time.time()
    
    matches = []
    deliveries = []
    
    for count, file_path in enumerate(files, 1):
        match_id = os.path.basename(file_path).split('.')[0]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            continue
            
        info = data.get("info", {})
        dates = info.get("dates", [])
        date = dates[0] if dates else None
        teams = info.get("teams", [])
        team1 = teams[0] if len(teams) > 0 else None
        team2 = teams[1] if len(teams) > 1 else None
        outcome = info.get("outcome", {})
        winner = outcome.get("winner")
        by = outcome.get("by", {})
        toss = info.get("toss", {})
        
        matches.append({
            "id": match_id,
            "city": info.get("city"),
            "date": date,
            "match_type": info.get("match_type"),
            "team1": team1,
            "team2": team2,
            "toss_winner": toss.get("winner"),
            "toss_decision": toss.get("decision"),
            "winner": winner,
            "win_by_runs": by.get("runs"),
            "win_by_wickets": by.get("wickets"),
            "player_of_match": info.get("player_of_match", [None])[0],
            "venue": info.get("venue")
        })
        
        innings = data.get("innings", [])
        for inning_idx, inning in enumerate(innings):
            inning_num = inning_idx + 1
            for over in inning.get("overs", []):
                over_num = over.get("over")
                for ball_idx, delivery in enumerate(over.get("deliveries", []), 1):
                    actual_del = delivery.get("actual_delivery", "")
                    if "." in str(actual_del):
                        try:
                            ball_val = int(str(actual_del).split(".")[1])
                        except Exception:
                            ball_val = ball_idx
                    else:
                        ball_val = ball_idx
                        
                    runs = delivery.get("runs", {})
                    wickets = delivery.get("wickets", [])
                    extras = delivery.get("extras", {})
                    
                    deliveries.append({
                        "match_id": match_id,
                        "inning": inning_num,
                        "over": over_num,
                        "ball": ball_val,
                        "batter": delivery.get("batter"),
                        "bowler": delivery.get("bowler"),
                        "non_striker": delivery.get("non_striker"),
                        "runs_batter": runs.get("batter", 0),
                        "runs_extras": runs.get("extras", 0),
                        "runs_total": runs.get("total", 0),
                        "player_dismissed": wickets[0].get("player_out") if wickets else None,
                        "dismissal_kind": wickets[0].get("kind") if wickets else None,
                        "extras_type": list(extras.keys())[0] if extras else None
                    })
                    
        if count % 500 == 0 or count == len(files):
            print(f"Parsed {count}/{len(files)} JSON files in {time.time() - t0:.2f}s...")
            
    print(f"Writing {len(matches)} matches and {len(deliveries)} deliveries into SQLite DB...")
    df_matches = pd.DataFrame(matches)
    df_deliveries = pd.DataFrame(deliveries)
    
    # Save to SQLite tables replacing existing sample data
    df_matches.to_sql("matches", con=engine, if_exists="replace", index=False)
    df_deliveries.to_sql("deliveries", con=engine, if_exists="replace", index=False)
    
    print(f"Extraction complete in {time.time() - t0:.2f}s!")

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    parse_json_to_db(limit=limit)
