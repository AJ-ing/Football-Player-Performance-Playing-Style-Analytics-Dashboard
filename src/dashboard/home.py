import streamlit as st
import pandas as pd

def render(df: pd.DataFrame):
    st.title("⚽ Football Player Performance & Playing Style Analytics")
    
    st.markdown("---")
    
    # 1. KPIs Section
    st.header("Dataset Overview")
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Players", f"{len(df):,}")
            
        with col2:
            st.metric("Leagues/Competitions", "Multiple") # Transfermarkt spans many
            
        with col3:
            st.metric("Total Goals", f"{int(df['goals'].sum()):,}")
            
        with col4:
            st.metric("Unique Archetypes", len(df['cluster_archetype'].unique()) if 'cluster_archetype' in df.columns else 0)
    else:
        st.warning("No data available to display KPIs.")
        
    st.markdown("---")
    
    # 2. Methodology Section
    st.header("Methodology")
    st.markdown("""
    Welcome to the Football Analytics Dashboard! This tool is designed to move beyond basic counting stats 
    and uncover the underlying **playing styles** of football players using Machine Learning.
    
    ### How It Works
    
    1. **Data Ingestion & Cleaning:** We ingest player and appearance data from Transfermarkt. Players with fewer than 450 minutes played are filtered out to remove statistical noise.
    2. **Feature Engineering:** Raw stats (goals, assists, cards, minutes) are converted into **per-90-minute** rates. We also construct composite indices (Offensive Index, Defensive Index) to summarize a player's overall contribution on both ends of the pitch.
    3. **Machine Learning (Clustering):**
       - **Scaling:** We use a `RobustScaler` to normalize the data. This prevents players with extreme outlier stats (like a striker scoring 40 goals) from warping the analysis.
       - **K-Means Algorithm:** We apply K-Means clustering (default K=5) to group players strictly based on their playing style metrics (excluding age and market value from the algorithm to prevent bias).
       - **Archetyping:** The clusters are then analyzed and assigned descriptive labels (e.g., "Attackers", "Defenders") based on their dominant statistical traits.
    4. **Similarity Engine:** Using Euclidean distance across the scaled feature space, the system can instantly find the closest matches to any given player's unique playing style profile.
    
    ### Navigation
    - **Player Explorer:** Search for specific players, filter by position/age/value, compare players side-by-side on a radar chart, and discover statistically similar players.
    - **Cluster Explorer:** Visualize the entire player population on a 2D scatter plot to see how different archetypes separate from one another.
    - **Statistics:** View distributions of key performance metrics across the dataset.
    """)
