import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.score_prediction.train import train_all_models

if __name__ == "__main__":
    print("Starting ML Model Retraining...")
    results = train_all_models()
    print("\nRetraining complete! Summary:")
    print(results)
