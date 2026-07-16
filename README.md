# ⚽ Football Player Performance & Playing Style Analytics Dashboard

An end-to-end data pipeline and Streamlit dashboard that analyzes football player performance, engineers custom playing style metrics, and clusters players using Machine Learning (K-Means) to identify unique stylistic archetypes.

## 🚀 Deployment

The dashboard is designed to be deployed on **Streamlit Community Cloud**.

**Live URL:** [Insert Streamlit Cloud URL Here]

> **Note on Architecture:** To respect the 1GB memory limits of the free tier of Streamlit Cloud, the data cleaning and clustering pipeline must be run **locally**. The dashboard itself is lightweight and serves the pre-computed static artifacts (`data/processed/players.parquet` and `models/kmeans_model.pkl`).

## 📸 Screenshots

*(Replace the placeholder images below with actual screenshots of your dashboard)*

### Player Explorer & Comparison
![Player Explorer Screenshot](docs/assets/placeholder_player_explorer.png)

### Cluster Archetype Analysis
![Cluster Explorer Screenshot](docs/assets/placeholder_cluster_explorer.png)

### Correlation Heatmaps
![Statistics Screenshot](docs/assets/placeholder_statistics.png)

## 🛠️ Features

* **Custom Feature Engineering:** Converts raw counting stats into per-90 metrics and computes custom indices (e.g., Composite Offensive Index, Composite Defensive Index, Shot Conversion Rate).
* **Machine Learning Archetypes:** Uses `RobustScaler` and `K-Means` clustering (default K=5) to dynamically assign players into descriptive stylistic groups (e.g., Attackers, Defenders).
* **Similarity Engine:** Uses Euclidean distance to instantly find the top 5 statistically similar players to any given target.
* **Premium Dashboard:** Built with Streamlit, custom CSS, Google Fonts (Outfit), and a sleek dark-mode aesthetic featuring Plotly interactive charts.

## 💻 Local Setup & Execution

### 1. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/AJ-ing/Football-Player-Performance-Playing-Style-Analytics-Dashboard.git
cd Football-Player-Performance-Playing-Style-Analytics-Dashboard/repo
pip install -r requirements.txt
```

### 2. Run the Data Pipeline
Before launching the dashboard, you must run the pipeline locally to extract the data, clean it, and generate the clustered model artifacts.
```bash
python scripts/run_pipeline.py
```
*This will generate `data/processed/players.parquet` and `models/kmeans_model.pkl`.*

### 3. Launch the Dashboard
Once the artifacts are generated, spin up the Streamlit UI:
```bash
streamlit run app.py
```

### 4. Running Tests
The project maintains a rigorous unit testing and smoke testing suite via Pytest.
```bash
pytest
```

## 📂 Project Structure

```text
├── app.py                     # Streamlit UI Entry Point
├── requirements.txt           # Python Dependencies
├── README.md                  # Documentation
├── scripts/
│   └── run_pipeline.py        # E2E Data & ML Pipeline Script
├── src/
│   ├── data_loader.py         # Data Ingestion
│   ├── preprocessing.py       # Cleaning & Validation
│   ├── feature_engineering.py # Custom Metrics Calculation
│   ├── clustering.py          # K-Means & Scaling
│   ├── similarity.py          # Euclidean Distance Engine
│   ├── visualization.py       # Plotly Chart Generators
│   └── dashboard/             # Streamlit Page Modules
│       ├── home.py
│       ├── player_explorer.py
│       ├── cluster_explorer.py
│       ├── statistics.py
│       └── settings.py
├── data/
│   ├── raw/                   # Ignored via .gitignore
│   └── processed/             # Output Artifacts (parquet)
└── models/                    # Output Artifacts (pkl)
```

## ⚖️ License
[Insert License Here]