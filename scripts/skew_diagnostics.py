import os
import sys
import logging
import pandas as pd
from scipy.stats import skew

# Ensure src can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_dataset
from src.preprocessing import clean_data
from src.feature_engineering import engineer_features

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/skew_report.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def run_diagnostics(data_dir: str):
    print("Loading dataset...")
    df = load_dataset(data_dir)
    print("Cleaning dataset...")
    df = clean_data(df)
    print("Engineering features...")
    df = engineer_features(df)
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    logging.info("--- Skewness Diagnostic Report ---")
    print("\n--- Skewness Diagnostic Report ---")
    for col in numeric_cols:
        col_skew = skew(df[col].dropna())
        msg = f"Feature: {col:<25} | Skewness: {col_skew:.3f}"
        logging.info(msg)
        print(msg)
        
    print("\nDiagnostics complete. Check logs/skew_report.log")

if __name__ == "__main__":
    run_diagnostics('data/raw')
