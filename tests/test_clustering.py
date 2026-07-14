import pytest
import pandas as pd
import numpy as np
from src.clustering import perform_clustering

def test_perform_clustering():
    # Create dummy dataframe with enough rows for K=2
    data = {
        'player_id': [1, 2, 3, 4],
        'goals_per_90': [0.1, 0.9, 0.8, 0.2],
        'assists_per_90': [0.2, 0.8, 0.7, 0.1],
        'composite_offensive_index': [0.3, 1.7, 1.5, 0.3],
        'composite_defensive_index': [1.5, 0.2, 0.3, 1.4]
    }
    df = pd.DataFrame(data)
    
    # We don't save the model here, just test the return frame
    clustered_df = perform_clustering(df, n_clusters=2)
    
    # Check that 'cluster' and 'cluster_archetype' columns are added
    assert 'cluster' in clustered_df.columns
    assert 'cluster_archetype' in clustered_df.columns
    
    # Check that exactly 2 clusters are formed
    assert len(clustered_df['cluster'].unique()) == 2
