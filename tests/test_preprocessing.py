import pandas as pd
import numpy as np
import pytest
from src.preprocessing import clean_data

def test_clean_data_handles_missing_criticals():
    data = {
        'player_id': [1, 2],
        'name': ['Player A', None],
        'current_club_name': ['Club A', 'Club B'],
        'position': ['Attack', 'Defender'],
        'date_of_birth': ['2000-01-01', '1995-05-05'],
        'market_value_in_eur': [1000, 2000]
    }
    df = pd.DataFrame(data)
    cleaned = clean_data(df)
    
    # Should drop Player B due to missing name
    assert len(cleaned) == 1
    assert cleaned.iloc[0]['name'] == 'Player A'

def test_clean_data_imputes_missing_metrics():
    data = {
        'player_id': [1],
        'name': ['Player A'],
        'current_club_name': ['Club A'],
        'position': ['Attack'],
        'date_of_birth': ['2000-01-01'],
        'market_value_in_eur': [1000],
        'goals': [None],
        'assists': [np.nan if 'np' in globals() else pd.NA],
        'minutes_played': [90],
        'yellow_cards': [0],
        'red_cards': [0]
    }
    df = pd.DataFrame(data)
    cleaned = clean_data(df)
    
    assert cleaned.iloc[0]['goals'] == 0
    assert cleaned.iloc[0]['assists'] == 0
    
def test_clean_data_deduplicates():
    data = {
        'player_id': [1, 1],
        'name': ['Player A', 'Player A'],
        'current_club_name': ['Club A', 'Club A'],
        'position': ['Attack', 'Attack'],
        'date_of_birth': ['2000-01-01', '2000-01-01'],
        'market_value_in_eur': [1000, 1000]
    }
    df = pd.DataFrame(data)
    cleaned = clean_data(df)
    assert len(cleaned) == 1
