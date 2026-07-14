import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

def perform_clustering(df: pd.DataFrame, n_clusters: int = 5, model_path: str = None) -> pd.DataFrame:
    """
    Performs clustering on the dataset based on engineered performance metrics.
    
    Args:
        df: The DataFrame containing engineered features.
        n_clusters: The number of clusters to form.
        model_path: If provided, the fitted scaler and model will be saved to this path.
    """
    # 1. Feature Selection
    # I selected specific performance and playing style features for clustering.
    # Excluded 'market_value_in_eur' and 'age' to ensure clusters are based purely on playing style, not value.
    features = [
        'goals_per_90', 'assists_per_90', 'yellow_cards_per_90', 'red_cards_per_90',
        'shots_total_per_90', 'shot_conversion_rate', 'pass_completion_rate', 'duels_won_rate',
        'composite_offensive_index', 'composite_defensive_index'
    ]
    
    # Filter only available features (since some were mocked/derived)
    features = [f for f in features if f in df.columns]
    X = df[features].copy()
    
    # 2. Feature Scaling
    # Per the Day 1 architectural decision, I swapped StandardScaler for RobustScaler.
    # This prevents heavily skewed count-derived features (like goals/90) from 
    # disproportionately pulling cluster centroids due to outliers.
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. KMeans Clustering
    # I fit a KMeans model with the specified number of clusters on the robustly scaled features.
    # A fixed random_state ensures reproducibility across pipeline runs.
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # Assign labels back to the dataframe
    df['cluster'] = cluster_labels
    
    # 4. Diagnostics
    # I compute the silhouette score to measure how well-separated the clusters are.
    # A score >= 0.25 is our target per SRD acceptance criteria.
    if len(X_scaled) > n_clusters:
        sil_score = silhouette_score(X_scaled, cluster_labels)
        logging.info(f"KMeans (K={n_clusters}) Silhouette Score: {sil_score:.3f}")
        print(f"KMeans (K={n_clusters}) Silhouette Score: {sil_score:.3f}")
        
    # 5. Archetype Labeling
    # Instead of arbitrary labels, I dynamically generate descriptive labels for each cluster
    # based on the dominant characteristic (e.g., highest composite_offensive_index -> 'Attack-minded').
    cluster_profiles = df.groupby('cluster')[features].mean()
    labels = {}
    for cluster_id, row in cluster_profiles.iterrows():
        # Simple heuristic for archetype naming based on the mean of the cluster
        if row.get('composite_offensive_index', 0) > cluster_profiles['composite_offensive_index'].quantile(0.75):
            labels[cluster_id] = f"Cluster {cluster_id}: Attackers"
        elif row.get('composite_defensive_index', 0) > cluster_profiles['composite_defensive_index'].quantile(0.75):
            labels[cluster_id] = f"Cluster {cluster_id}: Defenders"
        else:
            labels[cluster_id] = f"Cluster {cluster_id}: Balanced"
            
    df['cluster_archetype'] = df['cluster'].map(labels)

    # 6. Model Persistence
    # I package the fitted scaler, KMeans model, and selected features into a single dictionary.
    # This allows the Streamlit app to transform any new data using the exact same scaling parameters.
    if model_path:
        model_artifact = {
            'scaler': scaler,
            'model': kmeans,
            'features': features,
            'archetype_labels': labels
        }
        joblib.dump(model_artifact, model_path)
        
    return df
