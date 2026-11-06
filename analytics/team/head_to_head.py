import pandas as pd
from typing import Dict, Any


def get_head_to_head(team1: str, team2: str, matches_df: pd.DataFrame, deliveries_df: pd.DataFrame = None) -> Dict[str, Any]:
    h2h_matches = matches_df[
        ((matches_df["team1"] == team1) & (matches_df["team2"] == team2)) |
        ((matches_df["team1"] == team2) & (matches_df["team2"] == team1))
    ]

    total = len(h2h_matches)
    team1_wins = int(len(h2h_matches[h2h_matches["winner"] == team1]))
    team2_wins = int(len(h2h_matches[h2h_matches["winner"] == team2]))
    no_results = total - team1_wins - team2_wins

    # Toss win analysis
    team1_toss = h2h_matches[h2h_matches["toss_winner"] == team1]
    team1_toss_wins = int(len(team1_toss[team1_toss["winner"] == team1]))
    team2_toss = h2h_matches[h2h_matches["toss_winner"] == team2]
    team2_toss_wins = int(len(team2_toss[team2_toss["winner"] == team2]))

    # Win by batting/fielding first
    bat_first_col = "toss_decision"
    team1_bat_first_wins = 0
    team1_field_first_wins = 0
    team2_bat_first_wins = 0
    team2_field_first_wins = 0

    if bat_first_col in h2h_matches.columns:
        for _, row in h2h_matches.iterrows():
            winner = row.get("winner", "")
            toss_w = row.get("toss_winner", "")
            decision = str(row.get(bat_first_col, "")).lower()
            if winner == team1:
                if (toss_w == team1 and decision == "bat") or (toss_w == team2 and decision == "field"):
                    team1_bat_first_wins += 1
                else:
                    team1_field_first_wins += 1
            elif winner == team2:
                if (toss_w == team2 and decision == "bat") or (toss_w == team1 and decision == "field"):
                    team2_bat_first_wins += 1
                else:
                    team2_field_first_wins += 1

    # Innings-level scoring per team
    team1_avg_score = 0.0
    team2_avg_score = 0.0
    team1_high = 0
    team2_high = 0

    if deliveries_df is not None and not h2h_matches.empty:
        h2h_ids = h2h_matches["id"].tolist()
        h2h_deliv = deliveries_df[deliveries_df["match_id"].isin(h2h_ids)]

        for team, col in [(team1, "team1"), (team2, "team2")]:
            # matches where this team batted first
            bat_matches_t1 = h2h_matches[h2h_matches["team1"] == team]["id"].tolist()
            bat_matches_t2 = h2h_matches[h2h_matches["team2"] == team]["id"].tolist()

            inn1_scores = h2h_deliv[
                (h2h_deliv["match_id"].isin(bat_matches_t1)) & (h2h_deliv["inning"] == 1)
            ].groupby("match_id")["runs_total"].sum()

            inn2_scores = h2h_deliv[
                (h2h_deliv["match_id"].isin(bat_matches_t2)) & (h2h_deliv["inning"] == 2)
            ].groupby("match_id")["runs_total"].sum()

            all_scores = pd.concat([inn1_scores, inn2_scores])
            avg_s = round(float(all_scores.mean()), 1) if len(all_scores) > 0 else 0.0
            high_s = int(all_scores.max()) if len(all_scores) > 0 else 0

            if team == team1:
                team1_avg_score = avg_s
                team1_high = high_s
            else:
                team2_avg_score = avg_s
                team2_high = high_s

    # Recent matches (last 10)
    recent = h2h_matches.tail(10)[
        ["id", "date", "venue", "winner", "win_by_runs", "win_by_wickets", "toss_winner", "toss_decision"]
    ].fillna(0)

    return {
        "team1": team1,
        "team2": team2,
        "total_matches": total,
        "team1_wins": team1_wins,
        "team2_wins": team2_wins,
        "no_results": no_results,
        "toss_analysis": {
            "team1_toss_wins": int(len(team1_toss)),
            "team1_wins_after_toss": team1_toss_wins,
            "team2_toss_wins": int(len(team2_toss)),
            "team2_wins_after_toss": team2_toss_wins,
        },
        "innings_batting": {
            "team1_avg_score": team1_avg_score,
            "team1_high": team1_high,
            "team2_avg_score": team2_avg_score,
            "team2_high": team2_high,
        },
        "first_innings_wins": {
            "team1_bat_first_wins": team1_bat_first_wins,
            "team1_field_first_wins": team1_field_first_wins,
            "team2_bat_first_wins": team2_bat_first_wins,
            "team2_field_first_wins": team2_field_first_wins,
        },
        "recent_matches": recent.to_dict(orient="records")
    }
