import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["platform"] == "CricketIQ AI"

def test_get_players_endpoint():
    response = client.get("/api/players/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_teams_endpoint():
    response = client.get("/api/teams/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_prediction_endpoint():
    payload = {
        "venue": "Melbourne Cricket Ground",
        "team1": "Australia",
        "team2": "Sri Lanka",
        "over": 10,
        "ball": 3,
        "cumulative_runs": 85,
        "cumulative_wickets": 2,
        "runs_last_5_overs": 42,
        "wickets_last_5_overs": 1,
        "model_name": "random_forest"
    }
    response = client.post("/api/prediction/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_final_score" in data
    assert data["model_used"] == "random_forest"
