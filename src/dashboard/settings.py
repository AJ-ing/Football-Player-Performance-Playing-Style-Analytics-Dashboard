import streamlit as st
import os

def render(df):
    st.header("Settings & Configuration")
    
    st.markdown("""
    This page displays the configuration parameters used to generate the currently loaded dataset.
    
    > [!IMPORTANT]
    > **Why is Live K-Means Adjustment Disabled?**  
    > The data cleaning and K-Means clustering algorithm requires significant computational memory. To ensure stability and prevent Out-Of-Memory (OOM) crashes on the Streamlit Cloud free tier, the machine learning pipeline runs locally, and this dashboard serves the pre-computed static artifacts (`models/kmeans_model.pkl` and `data/processed/players.parquet`).
    """)
    
    st.subheader("Current Pipeline Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Clustering K (Clusters)", value="5")
        st.metric(label="Minimum Minutes Played", value="450")
        
    with col2:
        st.metric(label="Scaler Engine", value="RobustScaler")
        st.metric(label="Distance Metric (Similarity)", value="Euclidean")
        
    st.divider()
    
    st.subheader("Artifact Status")
    
    parquet_exists = os.path.exists("data/processed/players.parquet")
    model_exists = os.path.exists("models/kmeans_model.pkl")
    
    st.write(f"✅ `players.parquet` {'Found' if parquet_exists else 'Missing'}")
    st.write(f"✅ `kmeans_model.pkl` {'Found' if model_exists else 'Missing'}")
