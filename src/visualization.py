import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_radar_chart(player_data: pd.Series, categories: list, title: str):
    """Creates a radar chart for a single player."""
    values = player_data[categories].values.flatten().tolist()
    
    # Close the loop
    values += [values[0]]
    cats_closed = categories + [categories[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=cats_closed,
        fill='toself',
        name=player_data.get('name', 'Player')
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values) * 1.2 if max(values) > 0 else 1])
        ),
        showlegend=False,
        title=title,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def create_comparison_radar_chart(player_data: pd.DataFrame, categories: list, title: str):
    """Creates a radar chart comparing multiple players."""
    fig = go.Figure()
    
    max_val = 0
    for _, row in player_data.iterrows():
        values = row[categories].values.flatten().tolist()
        max_val = max(max_val, max(values))
        values += [values[0]]
        cats_closed = categories + [categories[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=cats_closed,
            fill='toself',
            name=row.get('name', 'Player')
        ))
        
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max_val * 1.2 if max_val > 0 else 1])
        ),
        showlegend=True,
        title=title,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def create_cluster_scatter(df: pd.DataFrame, x_col: str, y_col: str, color_col: str = 'cluster_archetype'):
    """Creates a 2D scatter plot colored by cluster."""
    fig = px.scatter(
        df, 
        x=x_col, 
        y=y_col, 
        color=color_col,
        hover_data=['name', 'current_club_name', 'position', 'age'],
        title=f"Player Clusters: {x_col} vs {y_col}",
        template="plotly_white"
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig
