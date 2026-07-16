import os
import pytest
import pandas as pd
import joblib

def test_parquet_artifact_exists_and_loads():
    artifact_path = 'data/processed/players.parquet'
    # Check existence
    assert os.path.exists(artifact_path), f"Artifact missing: {artifact_path}"
    
    # Check loadability
    try:
        df = pd.read_parquet(artifact_path)
        assert not df.empty, "Parquet file is empty."
        # Verify critical columns exist
        critical_cols = ['player_id', 'name', 'cluster', 'cluster_archetype']
        for col in critical_cols:
            assert col in df.columns, f"Missing critical column: {col}"
    except Exception as e:
        pytest.fail(f"Failed to load parquet artifact: {e}")

def test_model_artifact_exists_and_loads():
    model_path = 'models/kmeans_model.pkl'
    # Check existence
    assert os.path.exists(model_path), f"Model missing: {model_path}"
    
    # Check loadability
    try:
        model_dict = joblib.load(model_path)
        assert 'scaler' in model_dict, "Scaler missing from model artifact"
        assert 'model' in model_dict, "KMeans model missing from artifact"
        assert 'features' in model_dict, "Features list missing from artifact"
    except Exception as e:
        pytest.fail(f"Failed to load model artifact: {e}")
