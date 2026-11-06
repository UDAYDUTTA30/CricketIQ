import os
import sys
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ml.score_prediction.dataset import load_and_split_dataset
from ml.score_prediction.preprocessing import build_preprocessor
from ml.score_prediction.model_registry import save_model

def train_all_models():
    print("Loading dataset...")
    X_train, X_test, y_train, y_test = load_and_split_dataset()
    
    models = {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "xgboost": XGBRegressor(n_estimators=100, learning_rate=0.08, random_state=42)
    }
    
    results = {}
    
    for name, regressor in models.items():
        print(f"\nTraining model: {name}...")
        preprocessor = build_preprocessor()
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", regressor)
        ])
        
        pipeline.fit(X_train, y_train)
        
        preds = pipeline.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        rmse = root_mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        
        print(f"[{name}] MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.4f}")
        
        save_model(pipeline, name)
        results[name] = {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "R2": round(r2, 4)}
        
    return results

if __name__ == "__main__":
    train_all_models()
