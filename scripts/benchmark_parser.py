import os
import json
import glob
import time
import pandas as pd

RAW_DATA_DIR = "data/raw/cricsheet_json"

def test_fast_parser():
    t0 = time.time()
    files = glob.glob(os.path.join(RAW_DATA_DIR, "*.json"))
    print(f"Found {len(files)} JSON files. Testing parsing speed...")
    
    matches = []
    deliveries = []
    
    for i, file_path in enumerate(files):
        match_id = os.path.basename(file_path).split('.')[0]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
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
        
        for inning_idx, inning in enumerate(data.get("innings", [])):
            inning_num = inning_idx + 1
            for over in inning.get("overs", []):
                over_num = over.get("over")
                for ball_idx, delivery in enumerate(over.get("deliveries", []), 1):
                    runs = delivery.get("runs", {})
                    wickets = delivery.get("wickets", [])
                    extras = delivery.get("extras", {})
                    
                    deliveries.append({
                        "match_id": match_id,
                        "inning": inning_num,
                        "over": over_num,
                        "ball": ball_idx,
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
                    
        if (i + 1) % 1000 == 0 or (i + 1) == len(files):
            print(f"Parsed {i + 1}/{len(files)} files in {time.time() - t0:.2f}s (Matches: {len(matches)}, Deliveries: {len(deliveries)})")

    df_m = pd.DataFrame(matches)
    df_d = pd.DataFrame(deliveries)
    print(f"Total time: {time.time() - t0:.2f}s")
    print(f"Matches DataFrame: {df_m.shape}")
    print(f"Deliveries DataFrame: {df_d.shape}")

if __name__ == "__main__":
    test_fast_parser()
