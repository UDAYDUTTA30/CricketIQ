from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

def build_preprocessor() -> ColumnTransformer:
    categorical_cols = ["venue", "team1", "team2"]
    numeric_cols = [
        "over",
        "ball",
        "current_over_float",
        "cumulative_runs",
        "cumulative_wickets",
        "current_run_rate",
        "runs_last_5_overs",
        "wickets_last_5_overs"
    ]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
            ("num", StandardScaler(), numeric_cols)
        ]
    )
    
    return preprocessor
