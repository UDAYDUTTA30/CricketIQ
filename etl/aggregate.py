import pandas as pd
import numpy as np
import logging

def aggregate_batter_stats(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates overall career batting metrics for each player."""
    logging.info("Aggregating batter statistics...")
    
    # Filter out wide balls for legal balls faced count
    legal_deliveries = deliveries_df[deliveries_df["extras_type"] != "wides"]
    
    batter_grp = deliveries_df.groupby("batter")
    legal_grp = legal_deliveries.groupby("batter")
    
    runs = batter_grp["runs_batter"].sum()
    balls = legal_grp["ball"].count().reindex(runs.index, fill_value=0)
    fours = batter_grp["is_boundary_four"].sum()
    sixes = batter_grp["is_boundary_six"].sum()
    dots = batter_grp["is_dot"].sum()
    
    # Count dismissals
    dismissals = deliveries_df[deliveries_df["player_dismissed"].notna()].groupby("player_dismissed")["match_id"].count()
    outs = dismissals.reindex(runs.index, fill_value=0)
    
    # Count innings
    innings_played = deliveries_df.groupby("batter")["match_id"].nunique()
    
    df = pd.DataFrame({
        "batter": runs.index,
        "innings": innings_played.values,
        "runs": runs.values,
        "balls": balls.values,
        "outs": outs.values,
        "fours": fours.values,
        "sixes": sixes.values,
        "dots": dots.values,
    })
    
    df["strike_rate"] = np.where(df["balls"] > 0, (df["runs"] / df["balls"] * 100).round(2), 0.0)
    df["average"] = np.where(df["outs"] > 0, (df["runs"] / df["outs"]).round(2), df["runs"].astype(float))
    df["boundary_percentage"] = np.where(df["runs"] > 0, (((df["fours"] * 4 + df["sixes"] * 6) / df["runs"]) * 100).round(2), 0.0)
    df["dot_percentage"] = np.where(df["balls"] > 0, ((df["dots"] / df["balls"]) * 100).round(2), 0.0)
    
    return df.sort_values(by="runs", ascending=False).reset_index(drop=True)

def aggregate_bowler_stats(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates overall career bowling metrics for each player."""
    logging.info("Aggregating bowler statistics...")
    
    # Exclude uncredited extras (byes, legbyes) from bowler's conceded runs
    conceded = deliveries_df[~deliveries_df["extras_type"].isin(["byes", "legbyes"])]
    bowler_conceded = conceded.groupby("bowler")["runs_total"].sum()
    
    # Legal balls (exclude wides and noballs)
    legal_deliveries = deliveries_df[~deliveries_df["extras_type"].isin(["wides", "noballs"])]
    legal_balls = legal_deliveries.groupby("bowler")["ball"].count()
    
    # Wickets (exclude run outs, retired hurt, etc.)
    bowler_wickets_df = deliveries_df[
        deliveries_df["dismissal_kind"].isin(["bowled", "caught", "lbw", "stumped", "caught and bowled", "hit wicket"])
    ]
    wickets = bowler_wickets_df.groupby("bowler")["is_wicket"].sum().reindex(bowler_conceded.index, fill_value=0)
    
    dots = legal_deliveries[legal_deliveries["runs_total"] == 0].groupby("bowler")["ball"].count().reindex(bowler_conceded.index, fill_value=0)
    innings_bowled = deliveries_df.groupby("bowler")["match_id"].nunique().reindex(bowler_conceded.index, fill_value=0)
    
    df = pd.DataFrame({
        "bowler": bowler_conceded.index,
        "innings": innings_bowled.values,
        "conceded": bowler_conceded.values,
        "legal_balls": legal_balls.reindex(bowler_conceded.index, fill_value=0).values,
        "wickets": wickets.values,
        "dots": dots.values
    })
    
    df["overs"] = (df["legal_balls"] // 6) + (df["legal_balls"] % 6) / 10.0
    overs_decimal = df["legal_balls"] / 6.0
    
    df["economy"] = np.where(overs_decimal > 0, (df["conceded"] / overs_decimal).round(2), 0.0)
    df["average"] = np.where(df["wickets"] > 0, (df["conceded"] / df["wickets"]).round(2), 0.0)
    df["strike_rate"] = np.where(df["wickets"] > 0, (df["legal_balls"] / df["wickets"]).round(2), 0.0)
    df["dot_percentage"] = np.where(df["legal_balls"] > 0, ((df["dots"] / df["legal_balls"]) * 100).round(2), 0.0)
    
    return df.sort_values(by="wickets", ascending=False).reset_index(drop=True)

def aggregate_team_stats(matches_df: pd.DataFrame, innings_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates team level win/loss and performance statistics."""
    logging.info("Aggregating team statistics...")
    
    teams = pd.concat([matches_df["team1"], matches_df["team2"]]).unique()
    team_stats = []
    
    for team in teams:
        played = matches_df[(matches_df["team1"] == team) | (matches_df["team2"] == team)]
        total_played = len(played)
        wins = len(matches_df[matches_df["winner"] == team])
        losses = total_played - wins
        win_pct = round((wins / total_played * 100), 2) if total_played > 0 else 0.0
        
        team_stats.append({
            "team": team,
            "matches_played": total_played,
            "wins": wins,
            "losses": losses,
            "win_percentage": win_pct
        })
        
    return pd.DataFrame(team_stats).sort_values(by="matches_played", ascending=False).reset_index(drop=True)

def aggregate_venue_stats(matches_df: pd.DataFrame, innings_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates venue statistics (avg 1st innings score, avg 2nd innings score, boundary stats)."""
    logging.info("Aggregating venue statistics...")
    
    # Merge matches with innings
    merged = innings_df.merge(matches_df[["id", "venue"]], left_on="match_id", right_on="id")
    
    venue_stats = []
    for venue, group in merged.groupby("venue"):
        matches_count = group["match_id"].nunique()
        
        first_inn = group[group["inning"] == 1]
        second_inn = group[group["inning"] == 2]
        
        avg_1st_score = round(first_inn["total_runs"].mean(), 2) if len(first_inn) > 0 else 0.0
        avg_2nd_score = round(second_inn["total_runs"].mean(), 2) if len(second_inn) > 0 else 0.0
        
        max_score = group["total_runs"].max()
        min_score = group["total_runs"].min()
        
        venue_stats.append({
            "venue": venue,
            "matches_played": matches_count,
            "avg_1st_inn_score": avg_1st_score,
            "avg_2nd_inn_score": avg_2nd_score,
            "highest_score": max_score,
            "lowest_score": min_score
        })
        
    return pd.DataFrame(venue_stats).sort_values(by="matches_played", ascending=False).reset_index(drop=True)
