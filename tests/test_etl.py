import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etl.transform import assign_match_phase, transform_data
from etl.validate import validate_raw_data

def test_assign_match_phase():
    assert assign_match_phase(2) == "Powerplay"
    assert assign_match_phase(5) == "Powerplay"
    assert assign_match_phase(8) == "Middle"
    assert assign_match_phase(14) == "Middle"
    assert assign_match_phase(16) == "Death"
    assert assign_match_phase(19) == "Death"

def test_validate_raw_data():
    matches_df = pd.DataFrame([{
        "id": "1001",
        "team1": "India",
        "team2": "Australia",
        "venue": "MCG",
        "date": "2023-01-01"
    }])
    deliveries_df = pd.DataFrame([{
        "match_id": "1001",
        "inning": 1,
        "over": 0,
        "ball": 1,
        "batter": "V Kohli",
        "bowler": "M Starc",
        "runs_total": 4
    }])
    assert validate_raw_data(matches_df, deliveries_df) is True

def test_validate_raw_data_missing_column():
    matches_df = pd.DataFrame([{"id": "1001"}])
    deliveries_df = pd.DataFrame([{"match_id": "1001"}])
    assert validate_raw_data(matches_df, deliveries_df) is False
