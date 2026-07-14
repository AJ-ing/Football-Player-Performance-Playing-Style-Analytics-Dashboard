import os
import pandas as pd
from typing import Tuple

class DataValidationError(Exception):
    """Custom exception raised for schema validation errors."""
    pass

def load_dataset(raw_dir: str) -> pd.DataFrame:
    """
    Loads and merges raw Transfermarkt datasets from the given directory.
    Aggregates appearances and joins with player metadata.
    """
    players_path = os.path.join(raw_dir, 'players.csv')
    appearances_path = os.path.join(raw_dir, 'appearances.csv')
    
    if not os.path.exists(players_path) or not os.path.exists(appearances_path):
        raise FileNotFoundError(f"Missing required CSV files in {raw_dir}")
        
    players_df = pd.read_csv(players_path)
    appearances_df = pd.read_csv(appearances_path)
    
    # Required columns in players.csv
    required_player_cols = ['player_id', 'name', 'current_club_name', 'position', 'date_of_birth', 'market_value_in_eur']
    for col in required_player_cols:
        if col not in players_df.columns:
            raise DataValidationError(f"Missing required column '{col}' in players.csv")
            
    # Required columns in appearances.csv
    required_app_cols = ['player_id', 'goals', 'assists', 'minutes_played', 'yellow_cards', 'red_cards']
    for col in required_app_cols:
        if col not in appearances_df.columns:
            raise DataValidationError(f"Missing required column '{col}' in appearances.csv")

    # Aggregate appearances by player_id
    agg_appearances = appearances_df.groupby('player_id').agg({
        'goals': 'sum',
        'assists': 'sum',
        'minutes_played': 'sum',
        'yellow_cards': 'sum',
        'red_cards': 'sum'
    }).reset_index()
    
    # Merge players with their aggregated stats
    merged_df = players_df.merge(agg_appearances, on='player_id', how='left')
    
    return merged_df
