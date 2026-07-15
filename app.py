import streamlit as st
import pandas as pd
import os
import sys

# Add src to path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.dashboard import player_explorer, cluster_explorer, home, statistics

st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply premium styling and typography
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Make metrics stand out */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sleek container styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    
    /* Sidebar gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
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
    page = st.sidebar.radio("Navigation", ["Home", "Player Explorer", "Cluster Explorer", "Statistics"])
    
    # Load Data once and cache it
    with st.spinner("Loading player data..."):
        df = load_processed_data()
        
    if df.empty:
        st.error("No data available. Please run the data pipeline first.")
        st.stop()
        
    # Router
    if page == "Home":
        home.render(df)
    elif page == "Player Explorer":
        player_explorer.render(df)
    elif page == "Cluster Explorer":
        cluster_explorer.render(df)
    elif page == "Statistics":
        statistics.render(df)
        
    st.sidebar.markdown("---")
    st.sidebar.info("Football Player Performance Analytics v1.0")

if __name__ == "__main__":
    main()
