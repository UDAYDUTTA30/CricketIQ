import pandas as pd
from typing import Dict, Any, List

def get_worm_chart_data(match_id: str, deliveries_df: pd.DataFrame) -> Dict[str, Any]:
    m_deliv = deliveries_df[deliveries_df["match_id"] == match_id]
    if m_deliv.empty:
        return {"error": f"Match {match_id} not found"}
        
    result = {}
    for inn in [1, 2]:
        inn_df = m_deliv[m_deliv["inning"] == inn]
        if inn_df.empty:
            continue
            
        over_runs = inn_df.groupby("over").agg(
            cumulative_runs=("cumulative_runs", "max"),
            cumulative_wickets=("cumulative_wickets", "max")
        ).reset_index()
        
        result[f"inning_{inn}"] = over_runs.to_dict(orient="records")
        
    return {"match_id": match_id, "worm_data": result}
