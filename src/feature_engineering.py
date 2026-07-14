import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame, min_minutes: int = 450) -> pd.DataFrame:
    """
    Derives analysis-oriented features and filters out players with low minutes.
    """
    # Filter by minimum minutes
    df = df[df['minutes_played'] >= min_minutes].copy()
    
    # Per-90 statistics
    metrics = ['goals', 'assists', 'yellow_cards', 'red_cards']
    for metric in metrics:
        df[f'{metric}_per_90'] = (df[metric] / df['minutes_played']) * 90
        
    # Composite Indices
    # In absence of deeper passing/defensive stats, we construct basic indices
    df['offensive_index'] = (df['goals_per_90'] * 0.7) + (df['assists_per_90'] * 0.3)
    df['discipline_index'] = (df['yellow_cards_per_90'] * 0.2) + (df['red_cards_per_90'] * 0.8)
    
    # Market Value per Age-Adjusted Index (simplified: just market_value / age)
    df['value_age_ratio'] = df['market_value_in_eur'] / df['age']
    
    # Handle any potential infinite or NaN values created by division
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)
    
    return df
