import os
import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from ml.score_prediction.dataset import load_and_split_dataset
from ml.score_prediction.preprocessing import build_preprocessor

def evaluate_and_generate_table():
    print("Loading dataset...")
    X_train, X_test, y_train, y_test = load_and_split_dataset()
    
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost Regressor": XGBRegressor(n_estimators=100, learning_rate=0.08, random_state=42)
    }
    
    results = []
    
    for name, regressor in models.items():
        preprocessor = build_preprocessor()
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", regressor)
        ])
        
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        
        mae = mean_absolute_error(y_test, preds)
        mse = mean_squared_error(y_test, preds)
        rmse = root_mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        
        results.append({
            "Model": name,
            "MAE": round(mae, 4),
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "R² Score": round(r2, 4)
        })
        
    df_results = pd.DataFrame(results)
    
    print("\n" + "="*70)
    print("        CRICKETIQ-AI MODEL EVALUATION & PERFORMANCE SUMMARY")
    print("="*70)
    print(df_results.to_string(index=False))
    print("="*70 + "\n")

if __name__ == "__main__":
    evaluate_and_generate_table()
