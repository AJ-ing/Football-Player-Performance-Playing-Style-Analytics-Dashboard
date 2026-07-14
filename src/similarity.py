import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

def find_similar_players(df: pd.DataFrame, player_id: int, features: list, top_n: int = 5) -> pd.DataFrame:
    """
    Finds the most similar players to a given player using Euclidean distance 
    in the provided feature space.
    
    Args:
        df: DataFrame containing the players and their features. Must include 'player_id'.
        player_id: The ID of the target player.
        features: The list of feature columns to calculate distance on.
        top_n: Number of similar players to return.
        
    Returns:
        DataFrame of the top_n most similar players, including their distance score.
    """
    if player_id not in df['player_id'].values:
        raise ValueError(f"Player ID {player_id} not found in the dataset.")
        
    # Extract the target player's feature vector
    target_player_data = df[df['player_id'] == player_id][features].values
    
    # Extract the feature matrix for all players
    all_players_data = df[features].values
    
    # Calculate Euclidean distances between the target player and all others
    # euclidean_distances returns a 2D array, we flatten it to 1D
    distances = euclidean_distances(target_player_data, all_players_data).flatten()
    
    # Create a temporary dataframe with distances to easily sort and filter
    dist_df = df.copy()
    dist_df['similarity_distance'] = distances
    
    # Remove the target player from the results (distance = 0)
    dist_df = dist_df[dist_df['player_id'] != player_id]
    
    # Sort by distance (lower is more similar) and get the top N
    similar_players = dist_df.sort_values('similarity_distance', ascending=True).head(top_n)
    
    return similar_players
