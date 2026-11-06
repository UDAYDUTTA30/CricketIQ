import sqlite3
import pandas as pd

conn = sqlite3.connect("data/database/cricketiq.db")
matches_cnt = pd.read_sql("SELECT count(*) as cnt FROM matches", conn).iloc[0,0]
deliveries_cnt = pd.read_sql("SELECT count(*) as cnt FROM deliveries", conn).iloc[0,0]
print(f"Matches in cricketiq.db: {matches_cnt}")
print(f"Deliveries in cricketiq.db: {deliveries_cnt}")

# Let's check match_types and date ranges
df_m = pd.read_sql("SELECT match_type, count(*) as cnt FROM matches GROUP BY match_type", conn)
print("Match types in DB:")
print(df_m)

# Let's check interim CSVs
if pd.io.common.file_exists("data/interim/matches.csv"):
    df_im = pd.read_csv("data/interim/matches.csv")
    print(f"Interim matches.csv: {len(df_im)} rows")
    print("Match types in interim matches.csv:")
    print(df_im["match_type"].value_counts())
    
# Check top batters in deliveries
df_top = pd.read_sql("SELECT batter, count(distinct match_id) as matches, sum(runs_batter) as runs FROM deliveries GROUP BY batter ORDER BY matches DESC LIMIT 15", conn)
print("Top 15 batters by matches in DB:")
print(df_top)

# Check H2H matches counts
df_h2h = pd.read_sql("""
SELECT team1, team2, count(*) as matches 
FROM matches 
GROUP BY team1, team2 
ORDER BY matches DESC 
LIMIT 15
""", conn)
print("Top 15 team matchups in DB:")
print(df_h2h)
