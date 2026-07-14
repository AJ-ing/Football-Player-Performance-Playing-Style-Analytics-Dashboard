import pytest
import pandas as pd
from src.similarity import find_similar_players

def test_find_similar_players():
    # Setup dummy data
    data = {
        'player_id': [101, 102, 103, 104],
        'feature1': [1.0, 1.1, 9.0, 1.2],
        'feature2': [2.0, 2.1, 8.0, 2.2]
    }
    df = pd.DataFrame(data)
    
    # 101, 102, and 104 are very similar. 103 is an outlier.
    # We query for player 101
    similar_df = find_similar_players(df, player_id=101, features=['feature1', 'feature2'], top_n=2)
    
    # Target player should not be in results
    assert 101 not in similar_df['player_id'].values
    
    # Check we got top 2
    assert len(similar_df) == 2
    
    # 102 should be the most similar, followed by 104
    assert similar_df.iloc[0]['player_id'] == 102
    assert similar_df.iloc[1]['player_id'] == 104
    
    # Check that distance metric is calculated
    assert 'similarity_distance' in similar_df.columns

def test_find_similar_players_not_found():
    df = pd.DataFrame({'player_id': [1], 'f1': [1]})
    with pytest.raises(ValueError):
        find_similar_players(df, player_id=999, features=['f1'])
