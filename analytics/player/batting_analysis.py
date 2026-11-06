import pandas as pd
import numpy as np
from typing import Dict, Any


def get_batter_summary(batter_name: str, deliveries_df: pd.DataFrame) -> Dict[str, Any]:
    b_df = deliveries_df[deliveries_df["batter"] == batter_name]
    if b_df.empty:
        return {"error": f"Player '{batter_name}' not found"}

    legal = b_df[b_df["extras_type"] != "wides"]

    # --- Basic Aggregates ---
    runs = int(b_df["runs_batter"].sum())
    balls = int(len(legal))
    fours = int((b_df["runs_batter"] == 4).sum())
    sixes = int((b_df["runs_batter"] == 6).sum())
    dots = int((b_df["runs_batter"] == 0).sum())

    # Dismissals
    all_dismissals = deliveries_df[deliveries_df["player_dismissed"] == batter_name]
    outs = int(len(all_dismissals))
    innings_matches = b_df["match_id"].unique()
    innings = int(len(innings_matches))

    sr = round((runs / balls * 100), 2) if balls > 0 else 0.0
    avg = round((runs / outs), 2) if outs > 0 else float(runs)

    # --- Innings-level stats (runs per match) ---
    innings_runs = b_df.groupby("match_id")["runs_batter"].sum()
    highest_score = int(innings_runs.max()) if len(innings_runs) > 0 else 0
    fifty_plus = int((innings_runs >= 50).sum())
    hundred_plus = int((innings_runs >= 100).sum())
    duck_count = int((innings_runs == 0).sum())

    # Recent form: last 5 innings
    recent_innings = innings_runs.tail(5)
    recent_form = [
        {"match_id": mid, "runs": int(r)}
        for mid, r in recent_innings.items()
    ]

    # --- Phase breakdown ---
    phase_stats = b_df.groupby("match_phase").agg(
        runs=("runs_batter", "sum"),
        balls=("ball", "count"),
        fours=("is_boundary_four", "sum"),
        sixes=("is_boundary_six", "sum"),
    ).reset_index()
    phase_stats["strike_rate"] = np.where(
        phase_stats["balls"] > 0,
        (phase_stats["runs"] / phase_stats["balls"] * 100).round(2),
        0.0
    )
    phase_stats = phase_stats.astype({
        "runs": int, "balls": int, "fours": int, "sixes": int
    })

    # --- vs Opposition breakdown ---
    # Merge match info to get opponent
    match_ids = b_df["match_id"].unique()
    opp_runs = []
    if "team1" in deliveries_df.columns:
        # If team info is embedded in deliveries_df
        batter_with_teams = b_df.copy()
        if "team1" in batter_with_teams.columns:
            for _, grp in batter_with_teams.groupby("team2"):
                r = int(grp["runs_batter"].sum())
                bl = int(len(grp[grp["extras_type"] != "wides"]))
                opp_runs.append({
                    "opponent": str(grp["team2"].iloc[0]),
                    "runs": r,
                    "balls": bl,
                    "strike_rate": round(r / bl * 100, 2) if bl > 0 else 0.0
                })

    return {
        "batter": batter_name,
        "innings": innings,
        "runs": runs,
        "balls": balls,
        "outs": outs,
        "not_outs": innings - outs,
        "average": avg,
        "strike_rate": sr,
        "highest_score": highest_score,
        "fifty_plus": fifty_plus,
        "hundred_plus": hundred_plus,
        "duck_count": duck_count,
        "fours": fours,
        "sixes": sixes,
        "dots": dots,
        "boundary_percentage": round(((fours * 4 + sixes * 6) / runs * 100), 2) if runs > 0 else 0.0,
        "recent_form": recent_form,
        "phase_breakdown": phase_stats.to_dict(orient="records"),
        "vs_opposition": opp_runs
    }
