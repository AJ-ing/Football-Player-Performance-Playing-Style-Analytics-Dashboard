import os
import sys
import logging
import argparse

# Ensure src can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_dataset
from src.preprocessing import clean_data
from src.feature_engineering import engineer_features
from src.clustering import perform_clustering

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def main(raw_dir='data/raw', processed_dir='data/processed', models_dir='models', k=5):
    print("--- Football Analytics Data Pipeline ---")
    
    # Ensure output directories exist
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Extraction
    print("1. Extracting data...")
    logging.info("Pipeline Start: Extraction")
    df = load_dataset(raw_dir)
    print(f"Loaded {len(df)} raw player records.")
    
    # 2. Cleaning
    print("2. Cleaning data...")
    logging.info("Pipeline Step: Cleaning")
    df = clean_data(df)
    print(f"Cleaned data: {len(df)} records remaining.")
    
    # 3. Feature Engineering
    print("3. Engineering features...")
    logging.info("Pipeline Step: Feature Engineering")
    df = engineer_features(df, min_minutes=450)
    print(f"Engineered features for {len(df)} players (>=450 mins).")
    
    # 4. Clustering & Machine Learning
    print(f"4. Performing K-Means Clustering (K={k})...")
    logging.info(f"Pipeline Step: Clustering (K={k})")
    model_path = os.path.join(models_dir, 'kmeans_model.pkl')
    df = perform_clustering(df, n_clusters=k, model_path=model_path)
    print(f"Clustering complete. Model saved to {model_path}.")
    
    # 5. Persistence
    print("5. Saving processed dataset...")
    logging.info("Pipeline Step: Persistence")
    output_path = os.path.join(processed_dir, 'players.parquet')
    df.to_parquet(output_path, index=False)
    print(f"Dataset successfully saved to {output_path}.")
    logging.info("Pipeline Complete.")
    
    print("\nPipeline execution finished successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the end-to-end data pipeline.")
    parser.add_argument("--k", type=int, default=5, help="Number of clusters for K-Means.")
    args = parser.parse_args()
    
    main(k=args.k)
