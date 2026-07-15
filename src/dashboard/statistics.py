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
