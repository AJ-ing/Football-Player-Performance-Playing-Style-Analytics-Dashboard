import streamlit as st
import pandas as pd
import os
import sys

# Add src to path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.dashboard import player_explorer, cluster_explorer

st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply basic styling to look premium
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .css-1d391kg {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_processed_data():
    """Loads the preprocessed and clustered parquet file."""
    data_path = 'data/processed/players.parquet'
    if not os.path.exists(data_path):
        return pd.DataFrame()
    
    try:
        df = pd.read_parquet(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def main():
    st.sidebar.title("⚽ Analytics Dashboard")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio("Navigation", ["Player Explorer", "Cluster Explorer"])
    
    # Load Data once and cache it
    with st.spinner("Loading player data..."):
        df = load_processed_data()
        
    if df.empty:
        st.error("No data available. Please run the data pipeline first.")
        st.stop()
        
    # Router
    if page == "Player Explorer":
        player_explorer.render(df)
    elif page == "Cluster Explorer":
        cluster_explorer.render(df)
        
    st.sidebar.markdown("---")
    st.sidebar.info("Football Player Performance Analytics v1.0")

if __name__ == "__main__":
    main()
