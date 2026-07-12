import os
import subprocess
import argparse
import zipfile
import sys

def download_kaggle_dataset(dataset: str, download_path: str):
    """
    Downloads a Kaggle dataset using the Kaggle CLI.
    Assumes kaggle.json is present in ~/.kaggle/ or KAGGLE_USERNAME / KAGGLE_KEY are set.
    """
    print(f"Downloading {dataset} to {download_path}...")
    
    # Ensure kaggle is installed
    try:
        import kaggle
    except ImportError:
        print("Kaggle library is not installed. Please install it using: pip install kaggle")
        sys.exit(1)
        
    os.makedirs(download_path, exist_ok=True)
    
    # Need to authenticate using the Kaggle API
    kaggle.api.authenticate()
    
    # Run the kaggle download
    print("Starting download via Kaggle API...")
    try:
        kaggle.api.dataset_download_files(dataset, path=download_path, unzip=True)
        print("Download and extraction completed successfully.")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Kaggle dataset.")
    parser.add_argument("--dataset", type=str, required=True, help="Kaggle dataset slug (e.g., davidcariboo/player-scores)")
    parser.add_argument("--path", type=str, default="data/raw", help="Path to download the dataset to")
    
    args = parser.parse_args()
    download_kaggle_dataset(args.dataset, args.path)
