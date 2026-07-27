import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def render(df: pd.DataFrame):
    # ─── HERO SECTION ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
        border-radius: 18px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        border: 1px solid #334155;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute; top: -40px; right: -40px;
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(0,210,255,0.12) 0%, transparent 70%);
            border-radius: 50%;
        "></div>
        <div style="
            position: absolute; bottom: -30px; left: 30%;
            width: 150px; height: 150px;
            background: radial-gradient(circle, rgba(58,123,213,0.10) 0%, transparent 70%);
            border-radius: 50%;
        "></div>
        <div style="position: relative; z-index: 1;">
            <h1 style="
                font-size: 2.6rem;
                font-weight: 800;
                background: linear-gradient(90deg, #00d2ff, #3a7bd5, #a855f7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0 0 0.5rem 0;
                letter-spacing: -0.5px;
            ">⚽ Football Analytics Dashboard</h1>
            <p style="
                color: #94a3b8;
                font-size: 1.1rem;
                margin: 0 0 1.2rem 0;
                max-width: 680px;
                line-height: 1.6;
            ">
                Discover player archetypes, compare performance metrics, and find statistically similar players —
                powered by <strong style="color:#00d2ff;">K-Means Machine Learning</strong> on Transfermarkt data.
            </p>
            <div style="display: flex; gap: 0.8rem; flex-wrap: wrap;">
                <span style="
                    background: rgba(0,210,255,0.12); color: #00d2ff;
                    padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.82rem;
                    border: 1px solid rgba(0,210,255,0.25); font-weight: 600;
                ">🤖 K-Means Clustering</span>
                <span style="
                    background: rgba(168,85,247,0.12); color: #a855f7;
                    padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.82rem;
                    border: 1px solid rgba(168,85,247,0.25); font-weight: 600;
                ">📊 Per-90 Metrics</span>
                <span style="
                    background: rgba(34,197,94,0.12); color: #22c55e;
                    padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.82rem;
                    border: 1px solid rgba(34,197,94,0.25); font-weight: 600;
                ">🔗 Similarity Engine</span>
                <span style="
                    background: rgba(251,146,60,0.12); color: #fb923c;
                    padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.82rem;
                    border: 1px solid rgba(251,146,60,0.25); font-weight: 600;
                ">🎯 Radar Comparison</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("⚠️ No data available. Please run `scripts/run_pipeline.py` first.")
        return

    # ─── KPI METRICS ─────────────────────────────────────────────────────────
    st.markdown("### 📈 Dataset at a Glance")

    total_players = len(df)
    total_goals = int(df['goals'].sum()) if 'goals' in df.columns else 0
    total_assists = int(df['assists'].sum()) if 'assists' in df.columns else 0
    total_minutes = int(df['minutes_played'].sum()) if 'minutes_played' in df.columns else 0
    n_clusters = df['cluster_archetype'].nunique() if 'cluster_archetype' in df.columns else 0
    n_positions = df['position'].nunique() if 'position' in df.columns else 0
    avg_age = round(df['age'].mean(), 1) if 'age' in df.columns else 0
    avg_market_val = df['market_value_in_eur'].mean() if 'market_value_in_eur' in df.columns else 0

    kpi_cols = st.columns(4)
    kpis = [
        ("🧑‍🤝‍🧑 Total Players",   f"{total_players:,}",        "Players qualifying the 450-min threshold"),
        ("⚽ Total Goals",         f"{total_goals:,}",          "Cumulative goals across all appearances"),
        ("🎯 Total Assists",       f"{total_assists:,}",        "Cumulative assists across all appearances"),
        ("🗂️ Player Archetypes",   str(n_clusters),            "Distinct playing-style clusters identified"),
    ]
    for col, (label, value, help_text) in zip(kpi_cols, kpis):
        with col:
            st.metric(label=label, value=value, help=help_text)

    kpi_cols2 = st.columns(4)
    kpis2 = [
        ("⏱️ Total Minutes",       f"{total_minutes:,}",       "Minutes played summed across all players"),
        ("🏷️ Positions Covered",   str(n_positions),           "Distinct position types in the dataset"),
        ("🎂 Avg Player Age",      f"{avg_age} yrs",           "Mean age across all analysed players"),
        ("💶 Avg Market Value",    f"€{avg_market_val/1e6:.1f}M", "Mean market value (EUR) in the dataset"),
    ]
    for col, (label, value, help_text) in zip(kpi_cols2, kpis2):
        with col:
            st.metric(label=label, value=value, help=help_text)

    st.markdown("---")

    # ─── TOP PERFORMERS ───────────────────────────────────────────────────────
    st.markdown("### 🏆 Top Performers")
    tp_tabs = st.tabs(["⚽ Goals per 90", "🎯 Assists per 90", "📈 Offensive Index", "💶 Market Value"])

    name_col = 'name' if 'name' in df.columns else df.columns[0]

    with tp_tabs[0]:
        if 'goals_per_90' in df.columns:
            top_g = df.nlargest(10, 'goals_per_90')[[name_col, 'position', 'current_club_name', 'goals_per_90']].reset_index(drop=True)
            top_g.index += 1
            top_g.columns = ['Player', 'Position', 'Club', 'Goals / 90']
            top_g['Goals / 90'] = top_g['Goals / 90'].round(3)
            fig = px.bar(top_g, x='Goals / 90', y='Player', orientation='h',
                         color='Goals / 90', color_continuous_scale='Blues',
                         text='Goals / 90', title="Top 10 — Goals per 90 Minutes")
            fig.update_layout(showlegend=False, coloraxis_showscale=False,
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color='#e2e8f0', height=380,
                              yaxis=dict(autorange='reversed'))
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

    with tp_tabs[1]:
        if 'assists_per_90' in df.columns:
            top_a = df.nlargest(10, 'assists_per_90')[[name_col, 'position', 'current_club_name', 'assists_per_90']].reset_index(drop=True)
            top_a.index += 1
            top_a.columns = ['Player', 'Position', 'Club', 'Assists / 90']
            top_a['Assists / 90'] = top_a['Assists / 90'].round(3)
            fig = px.bar(top_a, x='Assists / 90', y='Player', orientation='h',
                         color='Assists / 90', color_continuous_scale='Purples',
                         text='Assists / 90', title="Top 10 — Assists per 90 Minutes")
            fig.update_layout(showlegend=False, coloraxis_showscale=False,
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color='#e2e8f0', height=380,
                              yaxis=dict(autorange='reversed'))
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

    with tp_tabs[2]:
        if 'offensive_index' in df.columns:
            top_oi = df.nlargest(10, 'offensive_index')[[name_col, 'position', 'current_club_name', 'offensive_index']].reset_index(drop=True)
            top_oi.index += 1
            top_oi.columns = ['Player', 'Position', 'Club', 'Offensive Index']
            top_oi['Offensive Index'] = top_oi['Offensive Index'].round(3)
            fig = px.bar(top_oi, x='Offensive Index', y='Player', orientation='h',
                         color='Offensive Index', color_continuous_scale='Oranges',
                         text='Offensive Index', title="Top 10 — Composite Offensive Index")
            fig.update_layout(showlegend=False, coloraxis_showscale=False,
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color='#e2e8f0', height=380,
                              yaxis=dict(autorange='reversed'))
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

    with tp_tabs[3]:
        if 'market_value_in_eur' in df.columns:
            top_mv = df.nlargest(10, 'market_value_in_eur')[[name_col, 'position', 'current_club_name', 'market_value_in_eur']].reset_index(drop=True)
            top_mv.index += 1
            top_mv.columns = ['Player', 'Position', 'Club', 'Market Value (€)']
            top_mv['Market Value (€)'] = top_mv['Market Value (€)'].apply(lambda x: f"€{x/1e6:.1f}M")
            st.dataframe(top_mv, use_container_width=True)

    st.markdown("---")

    # ─── POSITION DISTRIBUTION ────────────────────────────────────────────────
    col_pos, col_arch = st.columns(2)

    with col_pos:
        st.markdown("### 🧩 Players by Position")
        if 'position' in df.columns:
            pos_counts = df['position'].value_counts().reset_index()
            pos_counts.columns = ['Position', 'Count']
            fig_pos = px.pie(pos_counts, names='Position', values='Count',
                             color_discrete_sequence=px.colors.sequential.Blues_r,
                             hole=0.45)
            fig_pos.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', font_color='#e2e8f0',
                legend=dict(orientation='v', x=1.02),
                height=380
            )
            fig_pos.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pos, use_container_width=True)

    with col_arch:
        st.markdown("### 🤖 Players by Archetype")
        if 'cluster_archetype' in df.columns:
            arch_counts = df['cluster_archetype'].value_counts().reset_index()
            arch_counts.columns = ['Archetype', 'Count']
            fig_arch = px.bar(arch_counts, x='Count', y='Archetype', orientation='h',
                              color='Count', color_continuous_scale='Viridis',
                              text='Count')
            fig_arch.update_layout(
                showlegend=False, coloraxis_showscale=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e2e8f0', height=380,
                yaxis=dict(autorange='reversed')
            )
            fig_arch.update_traces(textposition='outside')
            st.plotly_chart(fig_arch, use_container_width=True)

    st.markdown("---")

    # ─── AGE DISTRIBUTION ────────────────────────────────────────────────────
    if 'age' in df.columns:
        st.markdown("### 🎂 Age Distribution of Players")
        fig_age = px.histogram(df, x='age', nbins=25, color_discrete_sequence=['#3a7bd5'],
                               labels={'age': 'Age', 'count': 'Number of Players'},
                               title="How Old Are the Players in This Dataset?")
        fig_age.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', bargap=0.05, height=320
        )
        fig_age.add_vline(x=df['age'].mean(), line_dash='dash', line_color='#00d2ff',
                          annotation_text=f"Mean: {df['age'].mean():.1f} yrs",
                          annotation_font_color='#00d2ff')
        st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("---")

    # ─── METHODOLOGY OVERVIEW ────────────────────────────────────────────────
    st.markdown("### 🔬 How This Dashboard Works")
    m1, m2, m3, m4 = st.columns(4)

    def step_card(col, icon, step_num, title, body, color):
        col.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid #334155;
            border-top: 3px solid {color};
            border-radius: 12px;
            padding: 1.2rem;
            height: 100%;
        ">
            <div style="font-size:2rem; margin-bottom:0.4rem;">{icon}</div>
            <div style="color:{color}; font-size:0.72rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.3rem;">Step {step_num}</div>
            <div style="font-weight:700; font-size:0.95rem; color:#e2e8f0; margin-bottom:0.5rem;">{title}</div>
            <div style="color:#94a3b8; font-size:0.83rem; line-height:1.55;">{body}</div>
        </div>
        """, unsafe_allow_html=True)

    step_card(m1, "📥", 1, "Data Ingestion",
              "Raw CSVs from Transfermarkt (via Kaggle) are loaded, schema-validated, and merged: player bio + match appearances + valuations.",
              "#00d2ff")
    step_card(m2, "🧹", 2, "Cleaning & Filtering",
              "Missing values are imputed, duplicates removed, and players with <450 minutes played are excluded to eliminate small-sample noise.",
              "#22c55e")
    step_card(m3, "⚙️", 3, "Feature Engineering",
              "Raw stats are converted to per-90 rates (Goals/90, Assists/90). Composite indices (Offensive, Defensive) and efficiency ratios are then computed.",
              "#a855f7")
    step_card(m4, "🤖", 4, "K-Means Clustering",
              "RobustScaler normalises the features; K-Means groups players into archetypes. Elbow Method and Silhouette Score guide the choice of K.",
              "#fb923c")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── KEY METRICS GLOSSARY ────────────────────────────────────────────────
    st.markdown("### 📖 Key Metrics Glossary")
    with st.expander("Click to expand — definitions for all custom metrics used in this dashboard"):
        glossary_cols = st.columns(2)

        left_metrics = [
            ("⚽ Goals per 90", "goals ÷ minutes × 90",
             "Scoring rate normalised for playing time. Prevents high-minute players from appearing superior purely through volume."),
            ("🎯 Assists per 90", "assists ÷ minutes × 90",
             "Creative output rate. A player with 5 assists in 450 min is just as productive as one with 10 in 900 min."),
            ("📈 Offensive Index", "(goals/90 × 0.7) + (assists/90 × 0.3)",
             "Composite attacking contribution. Weighted toward direct goal threat over creativity."),
            ("🛡️ Defensive Index", "Weighted: tackles + interceptions + duels won per 90",
             "Composite defensive work-rate. Higher scores mean more active defensive involvement."),
        ]
        right_metrics = [
            ("🎯 Shot Conversion Rate", "goals ÷ total shots",
             "Finishing efficiency. A rate of 0.33 (1 in 3 shots) is world-class; 0.05 indicates a wasteful finisher."),
            ("✅ Pass Completion Rate", "passes completed ÷ passes attempted",
             "Distribution reliability and technical quality under pressure."),
            ("💪 Duels Won Rate", "duels won ÷ total duels",
             "Physical and aerial contest effectiveness — key for defenders and holding midfielders."),
            ("💶 Value-Age Ratio", "market value ÷ age",
             "Heuristic for high-potential prospects. A 20-year-old at €20M scores much higher than a 32-year-old at the same value."),
        ]

        with glossary_cols[0]:
            for name, formula, desc in left_metrics:
                st.markdown(f"""
                <div style="
                    background:rgba(255,255,255,0.02); border:1px solid #334155;
                    border-radius:10px; padding:0.9rem 1rem; margin-bottom:0.7rem;
                ">
                    <div style="font-weight:700; color:#e2e8f0; font-size:0.9rem;">{name}</div>
                    <div style="font-family:monospace; color:#00d2ff; font-size:0.78rem; margin:0.25rem 0;">{formula}</div>
                    <div style="color:#94a3b8; font-size:0.82rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        with glossary_cols[1]:
            for name, formula, desc in right_metrics:
                st.markdown(f"""
                <div style="
                    background:rgba(255,255,255,0.02); border:1px solid #334155;
                    border-radius:10px; padding:0.9rem 1rem; margin-bottom:0.7rem;
                ">
                    <div style="font-weight:700; color:#e2e8f0; font-size:0.9rem;">{name}</div>
                    <div style="font-family:monospace; color:#a855f7; font-size:0.78rem; margin:0.25rem 0;">{formula}</div>
                    <div style="color:#94a3b8; font-size:0.82rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ─── NAVIGATION GUIDE ────────────────────────────────────────────────────
    st.markdown("### 🧭 Where to Go Next")
    nav1, nav2, nav3, nav4 = st.columns(4)

    def nav_card(col, icon, title, desc, color):
        col.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.2rem;
            text-align: center;
            transition: all 0.2s;
        ">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">{icon}</div>
            <div style="font-weight:700; color:{color}; font-size:0.95rem; margin-bottom:0.4rem;">{title}</div>
            <div style="color:#94a3b8; font-size:0.82rem; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    nav_card(nav1, "🔎", "Player Explorer",
             "Search by name, filter by position, age & value, compare players head-to-head on a radar chart.",
             "#00d2ff")
    nav_card(nav2, "🌐", "Cluster Explorer",
             "Visualise all players on a 2D PCA scatter plot coloured by archetype and drill into any cluster.",
             "#a855f7")
    nav_card(nav3, "📊", "Statistics",
             "Explore metric distributions, box plots, and the correlation heatmap across positions.",
             "#22c55e")
    nav_card(nav4, "⚙️", "Settings",
             "Adjust the number of clusters (K), view Elbow/Silhouette diagnostics, and explore config.",
             "#fb923c")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── FOOTER ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        text-align: center;
        color: #475569;
        font-size: 0.8rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #1e293b;
        margin-top: 1rem;
    ">
        Data sourced from <strong>Transfermarkt</strong> via Kaggle (CC BY-SA 4.0) &nbsp;|&nbsp;
        Built with ❤️ using Streamlit, Plotly & Scikit-learn &nbsp;|&nbsp;
        <a href="https://football-player-performance-playing-style-analytics-dashboard.streamlit.app"
           style="color: #00d2ff; text-decoration: none;">
           🌐 Live App
        </a>
    </div>
    """, unsafe_allow_html=True)
