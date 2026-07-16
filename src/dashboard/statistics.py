import streamlit as st
import pandas as pd
import plotly.express as px

def render(df: pd.DataFrame):
    st.header("Dataset Statistics")
    st.markdown("Analyze the distribution of performance metrics across the player population.")
    
    if df is None or df.empty:
        st.error("No data available.")
        return
        
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    # Filter out ID columns for cleaner UI
    display_cols = [c for c in numeric_cols if not c.endswith('_id')]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution (Histogram)")
        hist_col = st.selectbox("Select metric for Histogram:", options=display_cols, index=display_cols.index('age') if 'age' in display_cols else 0)
        
        fig_hist = px.histogram(
            df, 
            x=hist_col, 
            nbins=30,
            title=f"Distribution of {hist_col}",
            template="plotly_dark",
            color_discrete_sequence=['#00d2ff']
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col2:
        st.subheader("Spread by Position (Box Plot)")
        box_col = st.selectbox("Select metric for Box Plot:", options=display_cols, index=display_cols.index('market_value_in_eur') if 'market_value_in_eur' in display_cols else 0)
        
        # Limit to top 6 positions to avoid overcrowded x-axis
        top_positions = df['position'].value_counts().nlargest(6).index.tolist()
        box_df = df[df['position'].isin(top_positions)]
        
        fig_box = px.box(
            box_df, 
            x='position', 
            y=box_col,
            title=f"{box_col} by Position",
            template="plotly_dark",
            color='position'
        )
        # Hide legend as x-axis already explains it
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
        
    st.divider()
    
    st.subheader("Summary Statistics")
    st.dataframe(df[display_cols].describe(), use_container_width=True)
    
    st.divider()
    
    st.subheader("Correlation Analysis")
    st.markdown("Explore how different performance metrics correlate with each other. Select the metrics you want to include in the heatmap.")
    
    # Default selection for heatmap
    default_corr_cols = [
        'goals_per_90', 'assists_per_90', 'composite_offensive_index',
        'composite_defensive_index', 'market_value_in_eur', 'age'
    ]
    available_corr_cols = [c for c in default_corr_cols if c in display_cols]
    
    selected_corr_cols = st.multiselect(
        "Select metrics for correlation heatmap:",
        options=display_cols,
        default=available_corr_cols if available_corr_cols else display_cols[:5]
    )
    
    if len(selected_corr_cols) >= 2:
        from src.visualization import create_correlation_heatmap
        fig_corr = create_correlation_heatmap(df, selected_corr_cols)
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Please select at least two metrics to view their correlations.")
