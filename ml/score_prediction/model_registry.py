import os
import joblib
from typing import Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")

def save_model(model: Any, model_name: str):
    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
    file_path = os.path.join(SAVED_MODELS_DIR, f"{model_name}.pkl")
    joblib.dump(model, file_path)
    print(f"Model saved to {file_path}")

def load_model(model_name: str) -> Any:
    file_path = os.path.join(SAVED_MODELS_DIR, f"{model_name}.pkl")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Model file not found at {file_path}")
    return joblib.load(file_path)
