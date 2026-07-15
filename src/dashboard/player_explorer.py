import streamlit as st
import pandas as pd
from src.visualization import create_radar_chart, create_comparison_radar_chart
import os

def render(df: pd.DataFrame):
    st.header("Player Explorer")
    st.markdown("Search, filter, and compare football players based on performance and playing style.")
    
    # Error boundary: ensure dataframe is valid
    if df is None or df.empty:
        st.error("Dataset could not be loaded. Please ensure the data pipeline has been run successfully.")
        return
        
    # Filters
    st.sidebar.header("Filters")
    
    # Position filter
    positions = ['All'] + sorted(df['position'].dropna().unique().tolist())
    selected_position = st.sidebar.selectbox("Position", positions)
    
    # Age filter
    min_age, max_age = int(df['age'].min()), int(df['age'].max())
    selected_age = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))
    
    # Market Value filter
    min_val, max_val = float(df['market_value_in_eur'].min()), float(df['market_value_in_eur'].max())
    selected_val = st.sidebar.slider("Market Value (€)", min_val, max_val, (min_val, max_val), step=100000.0, format="€%d")
    
    # Search
    search_query = st.sidebar.text_input("Search Player by Name")
    
    # Apply filters
    filtered_df = df.copy()
    if selected_position != 'All':
        filtered_df = filtered_df[filtered_df['position'] == selected_position]
    filtered_df = filtered_df[(filtered_df['age'] >= selected_age[0]) & (filtered_df['age'] <= selected_age[1])]
    filtered_df = filtered_df[(filtered_df['market_value_in_eur'] >= selected_val[0]) & (filtered_df['market_value_in_eur'] <= selected_val[1])]
    
    if search_query:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False, na=False)]
        
    st.write(f"Showing **{len(filtered_df)}** players matching criteria.")
    
    # Data Table
    display_cols = ['name', 'current_club_name', 'position', 'age', 'market_value_in_eur', 'cluster_archetype']
    st.dataframe(filtered_df[display_cols].head(100), use_container_width=True)
    
    # CSV Export
    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download filtered results as CSV",
            data=csv,
            file_name='filtered_players.csv',
            mime='text/csv',
        )
        
    st.divider()
    
    # Player Comparison
    st.subheader("Player Comparison")
    
    compare_names = st.multiselect(
        "Select up to 3 players to compare:",
        options=filtered_df['name'].tolist(),
        max_selections=3
    )
    
    if compare_names:
        compare_df = df[df['name'].isin(compare_names)]
        
        # Define categories for the radar chart based on engineered features
        radar_cats = [
            'goals_per_90', 'assists_per_90', 'shot_conversion_rate',
            'pass_completion_rate', 'duels_won_rate', 'yellow_cards_per_90'
        ]
        
        # Ensure all columns exist
        available_cats = [c for c in radar_cats if c in compare_df.columns]
        
        if available_cats:
            # Normalize for radar chart (0 to 1 scale across the current subset)
            norm_df = compare_df.copy()
            for cat in available_cats:
                max_c = df[cat].max()
                if max_c > 0:
                    norm_df[cat] = norm_df[cat] / max_c
            
            fig = create_comparison_radar_chart(norm_df, available_cats, "Normalized Playing Style Comparison")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Required performance metrics for comparison are missing.")
