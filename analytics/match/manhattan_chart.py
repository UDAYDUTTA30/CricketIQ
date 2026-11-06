import pandas as pd
from typing import Dict, Any

def get_manhattan_chart_data(match_id: str, deliveries_df: pd.DataFrame) -> Dict[str, Any]:
    m_deliv = deliveries_df[deliveries_df["match_id"] == match_id]
    if m_deliv.empty:
        return {"error": f"Match {match_id} not found"}
        
    result = {}
    for inn in [1, 2]:
        inn_df = m_deliv[m_deliv["inning"] == inn]
        if inn_df.empty:
            continue
            
        over_stats = inn_df.groupby("over").agg(
            runs=("runs_total", "sum"),
            wickets=("is_wicket", "sum")
        ).reset_index()
        
        result[f"inning_{inn}"] = over_stats.to_dict(orient="records")
        
    return {"match_id": match_id, "manhattan_data": result}
