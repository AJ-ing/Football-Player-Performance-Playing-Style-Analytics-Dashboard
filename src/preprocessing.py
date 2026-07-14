import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw data by handling missing values, standardizing categoricals, and type coercion.
    """
    # 1. Deduplication (player_id is the primary key)
    df = df.drop_duplicates(subset=['player_id']).copy()
    
    # 2. Type coercion & Age calculation
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
    df['age'] = 2024 - df['date_of_birth'].dt.year
    
    # 2.5 Standardize Categorical Labels (Position / Sub-position)
    # Ensure consistent naming for positions
    if 'sub_position' in df.columns:
        df['sub_position'] = df['sub_position'].str.replace('Centre Back', 'Centre-Back')
        df['sub_position'] = df['sub_position'].str.replace('CB', 'Centre-Back')
        df['sub_position'] = df['sub_position'].str.strip().fillna('Unknown')
    
    if 'position' in df.columns:
        df['position'] = df['position'].str.title().str.strip()
    
    # 3. Missing Value Handling
    
    # Drop rows missing critical identifiers
    critical_cols = ['name', 'current_club_name', 'position']
    df = df.dropna(subset=critical_cols)
    
    # Impute performance metrics with 0 where missing
    perf_cols = ['goals', 'assists', 'minutes_played', 'yellow_cards', 'red_cards']
    for col in perf_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
        
    # Categoricals to 'Unknown'
    cat_cols = ['foot', 'country_of_citizenship']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')
            
    # Market value imputation (median by position)
    if 'market_value_in_eur' in df.columns:
        df['market_value_in_eur'] = df.groupby('position')['market_value_in_eur'].transform(
            lambda x: x.fillna(x.median())
        )
        # If any still missing (e.g. whole position group is missing), fill with overall median
        df['market_value_in_eur'] = df['market_value_in_eur'].fillna(df['market_value_in_eur'].median())
    
    # Age imputation (median)
    df['age'] = df['age'].fillna(df['age'].median())

    return df
