import pandas as pd
import numpy as np
from src.feature_engineering import engineer_features

def test_engineer_features_min_minutes():
    data = {
        'player_id': [1, 2],
        'minutes_played': [500, 100],
        'goals': [5, 1],
        'assists': [2, 0],
        'yellow_cards': [1, 0],
        'red_cards': [0, 0],
        'market_value_in_eur': [1000000, 500000],
        'age': [25, 20]
    }
    df = pd.DataFrame(data)
    engineered = engineer_features(df, min_minutes=450)
    
    assert len(engineered) == 1
    assert engineered.iloc[0]['player_id'] == 1
    
def test_engineer_features_per_90_calculation():
    data = {
        'player_id': [1],
        'minutes_played': [900],
        'goals': [10],
        'assists': [5],
        'yellow_cards': [2],
        'red_cards': [1],
        'market_value_in_eur': [1000000],
        'age': [25]
    }
    df = pd.DataFrame(data)
    engineered = engineer_features(df, min_minutes=450)
    
    # 10 goals in 900 minutes -> 1 goal per 90
    assert engineered.iloc[0]['goals_per_90'] == 1.0
    # 5 assists in 900 minutes -> 0.5 assist per 90
    assert engineered.iloc[0]['assists_per_90'] == 0.5
    
def test_engineer_features_composite_indices():
    data = {
        'player_id': [1],
        'minutes_played': [900],
        'goals': [10],
        'assists': [10],
        'yellow_cards': [10],
        'red_cards': [0],
        'market_value_in_eur': [5000000],
        'age': [25]
    }
    df = pd.DataFrame(data)
    engineered = engineer_features(df, min_minutes=450)
    
    # 1 goal per 90, 1 assist per 90
    # offensive = 1*0.5 + 1*0.3 + 0 (shots) = 0.8
    assert engineered.iloc[0]['composite_offensive_index'] == 0.8
    
    # value_age_ratio = 5000000 / 25 = 200000
    assert engineered.iloc[0]['value_age_ratio'] == 200000.0
