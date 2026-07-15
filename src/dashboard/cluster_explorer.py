import streamlit as st
import pandas as pd
from src.visualization import create_cluster_scatter

def render(df: pd.DataFrame):
    st.header("Cluster Explorer")
    st.markdown("Explore playing style archetypes and visualize how players are distributed across different performance metrics.")
    
    if df is None or df.empty or 'cluster' not in df.columns:
        st.error("Clustered data could not be loaded. Please ensure the machine learning pipeline has been run.")
        return
        
    col1, col2 = st.columns(2)
    
    with col1:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        x_axis = st.selectbox("X-Axis", options=numeric_cols, index=numeric_cols.index('composite_offensive_index') if 'composite_offensive_index' in numeric_cols else 0)
        
    with col2:
        y_axis = st.selectbox("Y-Axis", options=numeric_cols, index=numeric_cols.index('composite_defensive_index') if 'composite_defensive_index' in numeric_cols else 1)
        
    st.markdown("### 2D Projection")
    fig = create_cluster_scatter(df, x_col=x_axis, y_col=y_axis, color_col='cluster_archetype')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Archetype Summaries")
    
    # Calculate means per cluster archetype
    st.write("Average metrics by Archetype:")
    metrics_to_show = [
        'goals_per_90', 'assists_per_90', 'composite_offensive_index', 
        'composite_defensive_index', 'value_age_ratio'
    ]
    avail_metrics = [m for m in metrics_to_show if m in df.columns]
    
    if avail_metrics:
        summary_df = df.groupby('cluster_archetype')[avail_metrics].mean().round(3)
        st.dataframe(summary_df, use_container_width=True)
