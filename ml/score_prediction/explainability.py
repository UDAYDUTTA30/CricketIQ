import os
import sys
import shap
import pandas as pd
import numpy as np
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from ml.score_prediction.model_registry import load_model

def get_shap_explanation(sample_dict: Dict[str, Any], model_name: str = "random_forest") -> Dict[str, Any]:
    model = load_model(model_name)
    
    input_data = pd.DataFrame([sample_dict])
    preprocessor = model.named_steps["preprocessor"]
    regressor = model.named_steps["regressor"]
    
    transformed_input = preprocessor.transform(input_data)
    
    explainer = shap.Explainer(regressor)
    shap_values = explainer(transformed_input)
    
    feature_names = preprocessor.get_feature_names_out()
    vals = shap_values.values[0]
    
    importance = [
        {"feature": name, "shap_value": round(float(val), 4)}
        for name, val in zip(feature_names, vals)
    ]
    
    # Sort by absolute impact
    importance = sorted(importance, key=lambda x: abs(x["shap_value"]), reverse=True)[:10]
    
    return {
        "model_name": model_name,
        "base_value": round(float(shap_values.base_values[0]), 2),
        "top_feature_contributions": importance
    }
