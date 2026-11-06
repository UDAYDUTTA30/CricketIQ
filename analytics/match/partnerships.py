import pandas as pd
from typing import Dict, Any, List

def get_match_partnerships(match_id: str, deliveries_df: pd.DataFrame) -> Dict[str, Any]:
    m_deliv = deliveries_df[deliveries_df["match_id"] == match_id].copy()
    if m_deliv.empty:
        return {"error": f"Match {match_id} not found"}
        
    partnerships = {}
    for inn in [1, 2]:
        inn_df = m_deliv[m_deliv["inning"] == inn].copy()
        if inn_df.empty:
            continue
            
        inn_df["wicket_group"] = inn_df["is_wicket"].cumsum().shift(1, fill_value=0)
        
        inn_partnerships = []
        for w_idx, group in inn_df.groupby("wicket_group"):
            batters = list(set(group["batter"].unique()).union(set(group["non_striker"].unique())))
            runs = group["runs_total"].sum()
            balls = len(group)
            
            inn_partnerships.append({
                "wicket": int(w_idx) + 1,
                "batters": batters,
                "runs": int(runs),
                "balls": int(balls)
            })
            
        partnerships[f"inning_{inn}"] = inn_partnerships
        
    return {"match_id": match_id, "partnerships": partnerships}
