import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame, min_minutes: int = 450) -> pd.DataFrame:
    """
    Derives analysis-oriented features and filters out players with low minutes.
    """
    # Filter by minimum minutes
    df = df[df['minutes_played'] >= min_minutes].copy()
    
    # Per-90 statistics
    metrics = ['goals', 'assists', 'yellow_cards', 'red_cards', 'shots_total']
    for metric in metrics:
        if metric in df.columns:
            df[f'{metric}_per_90'] = (df[metric] / df['minutes_played']) * 90
            
    # Ratio features
    if 'shots_total' in df.columns:
        df['shot_conversion_rate'] = np.where(df['shots_total'] > 0, df['goals'] / df['shots_total'], 0)
    
    if 'passes_attempted' in df.columns and 'passes_completed' in df.columns:
        df['pass_completion_rate'] = np.where(df['passes_attempted'] > 0, df['passes_completed'] / df['passes_attempted'], 0)
        
    if 'duels_total' in df.columns and 'duels_won' in df.columns:
        df['duels_won_rate'] = np.where(df['duels_total'] > 0, df['duels_won'] / df['duels_total'], 0)
        
    # Composite Indices
    # Note: TRD mentions tackles, interceptions, key passes etc. Given Transfermarkt data limitations,
    # we construct these indices from available and mocked data.
    offensive_components = 0
    if 'goals_per_90' in df.columns: offensive_components += df['goals_per_90'] * 0.5
    if 'assists_per_90' in df.columns: offensive_components += df['assists_per_90'] * 0.3
    if 'shots_total_per_90' in df.columns: offensive_components += df['shots_total_per_90'] * 0.2
    df['composite_offensive_index'] = offensive_components
    
    defensive_components = 0
    if 'duels_won_rate' in df.columns: defensive_components += df['duels_won_rate'] * 0.5
    # Since Transfermarkt doesn't have tackles/interceptions natively without heavy joining/scraping, 
    # we rely on discipline as an inverse indicator for some defensive robustness or just the duels.
    if 'yellow_cards_per_90' in df.columns: defensive_components -= df['yellow_cards_per_90'] * 0.1
    df['composite_defensive_index'] = defensive_components
    
    # Market Value per Age-Adjusted Index (simplified: just market_value / age)
    if 'market_value_in_eur' in df.columns and 'age' in df.columns:
        df['value_age_ratio'] = df['market_value_in_eur'] / df['age']
    
    # Handle any potential infinite or NaN values created by division
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)
    
    return df
