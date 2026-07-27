# ⚽ Football Player Performance & Playing Style Analytics Dashboard

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://football-player-performance-playing-style-analytics-dashboard.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.2+-orange.svg)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**🌐 Live App → [football-player-performance-playing-style-analytics-dashboard.streamlit.app](https://football-player-performance-playing-style-analytics-dashboard.streamlit.app)**

*An end-to-end data pipeline and interactive ML dashboard for football player performance analysis and playing style archetype discovery.*

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Key Metrics & Terminology](#-key-metrics--terminology-explained)
  - [Per-90 Metrics](#per-90-metrics)
  - [Efficiency Ratios](#efficiency-ratios)
  - [Composite Indices](#composite-indices)
  - [Machine Learning Terms](#machine-learning-terms)
  - [Football Positions Glossary](#football-positions-glossary)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Local Setup & Execution](#-local-setup--execution)
- [Data Source](#-data-source)
- [Technical Stack](#-technical-stack)
- [Methodology](#-methodology)
- [Skewness Report & Scaling Decision](#-skewness-report--scaling-decision)
- [Running Tests](#-running-tests)
- [Known Limitations](#-known-limitations)
- [Future Enhancements](#-future-enhancements)

---

## 🔍 Overview

As modern football becomes increasingly data-driven, scouts, coaches, and analysts need tools that go beyond raw statistics. This project provides an **end-to-end analytics platform** that:

1. **Ingests** raw Transfermarkt data (via Kaggle) covering player appearances, valuations, and biographical attributes.
2. **Cleans & Engineers** a suite of custom performance metrics that normalize for playing time and surface true playing style signals.
3. **Clusters** players using K-Means machine learning into distinct stylistic archetypes — so a scout can find "players who play like Toni Kroos" rather than just "players with high assists".
4. **Visualises** the results in a rich, interactive Streamlit dashboard — with player search, side-by-side radar chart comparisons, cluster scatter plots, and statistical distributions.

> **Design Philosophy:** Clusters are formed exclusively from on-pitch *performance* metrics. Market value and wages are deliberately excluded from the feature set so that clusters reflect *playing style*, not financial worth.

---

## 🌐 Live Demo

**👉 [https://football-player-performance-playing-style-analytics-dashboard.streamlit.app](https://football-player-performance-playing-style-analytics-dashboard.streamlit.app)**

> **Note on Architecture:** To respect the ~1 GB memory limit of Streamlit Community Cloud's free tier, the full data-cleaning and K-Means clustering pipeline runs **locally only**. The deployed dashboard is lightweight and serves pre-computed static artifacts (`data/processed/players.parquet` and `models/kmeans_model.pkl`) — it never re-fits a model at runtime.

---

## 🛠️ Features

| Feature | Description |
|---|---|
| 🔎 **Player Search** | Instant case-insensitive substring search by name, club, or nationality |
| 🎛️ **Multi-Criteria Filtering** | Filter by league, position, age range, market value, and cluster archetype simultaneously |
| 📊 **Radar Chart Comparison** | Select any 2+ players and visualise their normalised metrics head-to-head on a spider/radar chart |
| 🗂️ **Cluster Explorer** | Browse all player archetypes; see 2D PCA scatter plots coloured by cluster with dominant feature breakdowns |
| 🔗 **Similarity Engine** | Click "Find Similar Players" on any profile to instantly retrieve the top-5 nearest neighbours by Euclidean distance in standardised feature space |
| 📈 **Statistics Page** | Histograms, box plots, and distribution charts for any metric across positions and clusters |
| 🌡️ **Correlation Heatmap** | Visualise pairwise feature correlations to understand redundancy and multicollinearity |
| 💾 **CSV Export** | Download the currently filtered player table for offline analysis in Excel or other tools |
| ⚙️ **Settings / K-Tuning** | Adjust the number of clusters (K) and explore Elbow Method and Silhouette Score diagnostics |
| 📋 **About Page** | Full methodology summary, data source attribution, and known limitations |

---

## 📊 Key Metrics & Terminology Explained

This project introduces a range of custom metrics to surface playing style signals that raw box-score statistics miss. Below is a complete glossary.

---

### Per-90 Metrics

Raw counting statistics (e.g., total goals, total assists) are biased by playing time — a player who played 3,000 minutes will almost always have higher raw counts than a player who played 900 minutes, even if the second player is more productive per appearance.

**Per-90 normalisation** divides any raw count by the player's total minutes played and multiplies by 90 (the length of a standard match), producing a *rate* rather than a *count*.

| Metric | Formula | What It Tells You |
|---|---|---|
| **Goals per 90** | `(goals ÷ minutes_played) × 90` | Scoring rate, independently of total appearances |
| **Assists per 90** | `(assists ÷ minutes_played) × 90` | Creative output rate |
| **Yellow Cards per 90** | `(yellow_cards ÷ minutes_played) × 90` | Discipline / aggression tendency |
| **Red Cards per 90** | `(red_cards ÷ minutes_played) × 90` | Extreme discipline risk |

> **Minimum minutes threshold:** Players with fewer than **450 minutes** played (~5 full matches) are **excluded** from analysis. A player who scored 2 goals in 30 minutes would appear statistically elite, but this is a statistical artefact of a tiny sample. 450 minutes is the standard threshold used in football analytics to ensure statistical reliability.

---

### Efficiency Ratios

Efficiency ratios express output relative to opportunity or attempts, rather than absolute counts.

| Metric | Formula | What It Tells You |
|---|---|---|
| **Shot Conversion Rate** | `goals ÷ shots_total` | How clinical a finisher is — a striker scoring 1-in-3 is elite; 1-in-20 is poor regardless of total goals |
| **Pass Completion Rate** | `passes_completed ÷ passes_attempted` | Distribution reliability and technical passing quality |
| **Duels Won Rate** | `duels_won ÷ duels_total` | Physical contest effectiveness — relevant for defenders, holding midfielders, and pressing attackers |
| **Value-Age Ratio** | `market_value_in_eur ÷ age` | A heuristic for identifying high-potential prospects: a 20-year-old valued at €20M has a much higher ratio than a 30-year-old at the same valuation |

> **Important:** The Value-Age Ratio is used for exploratory filtering only and is **excluded from the clustering feature set** to keep archetypes style-based, not value-based.

---

### Composite Indices

Composite indices compress multiple individual metrics into a single interpretable score. They are used both for dashboard display and as clustering features.

| Index | Components & Weights | What It Tells You |
|---|---|---|
| **Composite Offensive Index** | `(goals_per_90 × 0.70) + (assists_per_90 × 0.30)` | Overall attacking contribution — weighted toward direct goal threat over creativity |
| **Composite Defensive Index** | `(tackles_per_90 × 0.35) + (interceptions_per_90 × 0.35) + (duels_won_rate × 0.30)` | Overall defensive work rate and effectiveness |
| **Discipline Index** | `(yellow_cards_per_90 × 0.20) + (red_cards_per_90 × 0.80)` | Risk-weighted disciplinary tendency (red cards weighted 4× higher as they directly impact matches) |

> **Note on weights:** Weights reflect established football analytics conventions (goal-threat prioritised over creativity in attacking output) and are configurable in `config/settings.yaml`.

---

### Machine Learning Terms

| Term | Plain-English Explanation |
|---|---|
| **K-Means Clustering** | An unsupervised ML algorithm that groups players into `K` clusters by minimising within-cluster distance. Players in the same cluster share similar statistical profiles — they play in a similar *style*. |
| **K (Number of Clusters)** | The number of player archetypes to create. Default is `K=6`. Too few clusters merge distinct styles; too many produce overly granular, unintuitive groups. |
| **Elbow Method** | A diagnostic that plots inertia (sum of squared distances from each point to its cluster centre) for K = 2 to 12. The "elbow" — where adding more clusters yields diminishing gains — suggests the optimal K. |
| **Silhouette Score** | A metric from -1 to 1 measuring how well-separated and cohesive clusters are. A score closer to 1 means players within a cluster are very similar to each other and very different from other clusters. **Target: ≥ 0.25** for real-world sports data. |
| **RobustScaler** | A feature-scaling method that uses the **median** and **IQR (interquartile range)** rather than mean and standard deviation. This makes K-Means centroids robust to extreme statistical outliers (e.g., a player who scored 50 goals in a season won't distort the entire scaling). |
| **StandardScaler** *(not used)* | An alternative scaler using mean and standard deviation. Sensitive to outliers — rejected here because football statistics like goals and market value are heavily right-skewed (see Skewness Report below). |
| **PCA (Principal Component Analysis)** | A technique that reduces many features down to 2 dimensions *for visualisation only* — it makes a 2D scatter plot possible. PCA is **not** applied before clustering; clustering uses all features so archetypes remain interpretable. |
| **Euclidean Distance** | The straight-line distance between two points in multi-dimensional space. Used by the Similarity Engine: players with a shorter Euclidean distance in standardised feature space have more similar statistical profiles. |
| **Feature Space** | The multi-dimensional "space" where each player is represented as a coordinate vector, with one dimension per input metric. Distance between players in this space represents statistical similarity. |
| **Inertia** | The within-cluster sum of squared distances from each data point to its assigned centroid. Lower inertia means a tighter, more cohesive cluster. Used in the Elbow Method. |
| **Centroid** | The geometric centre (mean position) of all players assigned to a given cluster. A cluster's centroid represents the "average" statistical profile for that archetype. |
| **Archetype Labelling** | After clustering, each cluster's centroid is compared to the overall population mean. The top 3-5 features where the centroid deviates most from the mean determine the human-readable label (e.g., "Clinical Finisher", "Defensive Anchor"). |

---

### Football Positions Glossary

| Abbreviation | Full Name | Role Description |
|---|---|---|
| **GK** | Goalkeeper | Last line of defence; shot-stopping, distribution, and commanding the penalty area |
| **CB** | Centre-Back | Central defender; aerial duels, interceptions, and blocking central attacks |
| **RB / LB** | Right/Left Back | Wide defenders who also support attacks down the flank |
| **WB** | Wing-Back | A wider, more attack-oriented full-back, common in 3-5-2 or 3-4-3 formations |
| **DM / CDM** | Defensive / Central Defensive Midfielder | Screens the back four; high tackle and interception rates; "holding midfielder" |
| **CM** | Central Midfielder | Box-to-box presence; balances attacking and defensive duties |
| **CAM / AM** | Central Attacking Midfielder | Creates chances behind the striker; high key-passes and assists |
| **RM / LM** | Right/Left Midfielder | Wide midfielders who provide width and crosses |
| **RW / LW** | Right/Left Winger | Wide attackers; dribbling, crossing, and cutting inside to shoot |
| **CF** | Centre-Forward | Target man or leading striker; high goals and aerial duel rates |
| **SS** | Second Striker | Drops deep to link play and support the CF; hybrid between CAM and CF |

---

## 🏗️ Architecture

The system follows a strict **layered architecture** with a critical deployment invariant: the cloud-deployed Streamlit app **never runs the ML pipeline**. It only reads pre-computed artifacts.

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL PIPELINE (Run Once)                 │
│                                                             │
│  Raw CSV  →  data_loader  →  preprocessing  →              │
│  feature_engineering  →  clustering (RobustScaler+KMeans)  │
│                             │                               │
│                  ┌──────────┴──────────┐                   │
│                  ↓                     ↓                   │
│     data/processed/players.parquet   models/kmeans_model.pkl │
└─────────────────────────────────────────────────────────────┘
                        │                     │
                        └─────────┬───────────┘
                                  │ committed to GitHub
                                  ↓
┌─────────────────────────────────────────────────────────────┐
│                 STREAMLIT CLOUD (Read-Only)                  │
│                                                             │
│  app.py  →  loads .parquet + .pkl  →  dashboard pages      │
│         →  visualization  →  similarity engine (read-only)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```text
Football-Player-Performance-Playing-Style-Analytics-Dashboard/
│
├── app.py                          # Streamlit entry point & page router
├── requirements.txt                # Pinned Python dependencies
├── pytest.ini                      # Pytest configuration
├── README.md                       # This file
├── LICENSE                         # MIT License
│
├── config/
│   └── settings.yaml               # Centralised config (paths, K, thresholds, weights)
│
├── assets/
│   ├── logo.png                    # Dashboard branding
│   └── styles.css                  # Custom dark-mode CSS theming
│
├── data/
│   ├── raw/                        # ⚠️ Gitignored — raw Kaggle CSVs (never committed)
│   │   ├── players.csv
│   │   ├── appearances.csv
│   │   └── player_valuations.csv
│   ├── interim/                    # ⚠️ Gitignored — intermediate checkpoints
│   └── processed/                  # ✅ Committed — analysis-ready parquet artifacts
│       └── players.parquet
│
├── models/
│   └── kmeans_model.pkl            # ✅ Committed — fitted RobustScaler + KMeans model
│
├── notebooks/
│   ├── 01_eda.ipynb                # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb
│   └── 03_clustering_experiments.ipynb
│
├── scripts/
│   ├── download_data.py            # Kaggle API dataset downloader
│   ├── run_pipeline.py             # End-to-end pipeline: raw → processed + model
│   └── skew_diagnostics.py         # Logs skewness per feature (informs scaling choice)
│
├── src/
│   ├── __init__.py
│   ├── config.py                   # Config loader (YAML + env var overrides)
│   ├── data_loader.py              # CSV ingestion, schema validation, merge
│   ├── preprocessing.py            # Cleaning: missing values, dedup, categoricals
│   ├── feature_engineering.py      # Per-90 stats, ratios, composite indices
│   ├── clustering.py               # RobustScaler → KMeans → Elbow/Silhouette → labels
│   ├── similarity.py               # Euclidean distance nearest-neighbour search
│   ├── visualization.py            # Plotly/Seaborn chart builders (facade pattern)
│   ├── utils.py                    # Logging, caching wrappers, CSV export sanitisation
│   └── dashboard/
│       ├── __init__.py
│       ├── home.py                 # KPI summary page
│       ├── player_explorer.py      # Search, filter, profile, similarity
│       ├── cluster_explorer.py     # PCA scatter, archetype breakdown
│       ├── statistics.py           # Distribution charts
│       ├── visual_analytics.py     # Correlation heatmap
│       ├── data_download.py        # CSV export page
│       ├── about.py                # Methodology & data source page
│       └── settings.py             # K-tuning & recomputation (session-only)
│
├── tests/
│   ├── fixtures/
│   │   └── sample_players.csv      # Deterministic fixture dataset for unit tests
│   ├── test_preprocessing.py
│   ├── test_feature_engineering.py
│   ├── test_clustering.py
│   ├── test_similarity.py
│   └── test_utils.py
│
├── docs/
│   ├── 01-Software-Requirements-Document.md
│   ├── 02-Technical-Requirements-Document.md
│   └── 03-Software-Architecture-Document.md
│
└── deployment/
    ├── Dockerfile                  # Optional Docker image for self-hosted deployment
    ├── docker-compose.yml
    └── streamlit_config.toml       # Streamlit server & theme settings
```

---

## 💻 Local Setup & Execution

### Prerequisites

- Python 3.10+
- A [Kaggle account](https://www.kaggle.com) with an API key (`kaggle.json`)

### 1. Clone & Install

```bash
git clone https://github.com/AJ-ing/Football-Player-Performance-Playing-Style-Analytics-Dashboard.git
cd Football-Player-Performance-Playing-Style-Analytics-Dashboard/repo

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Download the Dataset

Place your `kaggle.json` API key in `~/.kaggle/` (macOS/Linux) or `%USERPROFILE%\.kaggle\` (Windows), then run:

```bash
python scripts/download_data.py --dataset davidcariboo/player-scores
```

This downloads and extracts all CSVs into `data/raw/`.

### 3. Run the Full Pipeline

```bash
python scripts/run_pipeline.py
```

This executes the complete pipeline:
- Load & validate raw CSVs
- Clean and normalise data
- Engineer per-90 and composite features
- Log skewness diagnostics to `logs/skew_report.log`
- Scale with `RobustScaler` and cluster with `KMeans`
- Write `data/processed/players.parquet` and `models/kmeans_model.pkl`

### 4. Launch the Dashboard Locally

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

---

## 📦 Data Source

| Field | Detail |
|---|---|
| **Source** | [Transfermarkt](https://www.transfermarkt.com) via Kaggle — [`davidcariboo/player-scores`](https://www.kaggle.com/datasets/davidcariboo/player-scores) |
| **License** | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — attribution required, redistribution permitted under same license |
| **Key Files Used** | `players.csv` (biography + market value), `appearances.csv` (match stats), `player_valuations.csv` (historical value) |
| **Coverage** | Top European leagues + international competitions; updated periodically by the dataset maintainer |
| **Raw Data Status** | **Not committed to the repository** — download locally using `scripts/download_data.py` |

---

## 🔬 Technical Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.10+ | Primary implementation language |
| Data Manipulation | Pandas, NumPy | DataFrame operations, vectorised computations |
| Machine Learning | Scikit-learn | `RobustScaler`, `KMeans`, `PCA`, `silhouette_score` |
| Statistics | SciPy | Skewness diagnostics (`scipy.stats.skew`) |
| Visualisation | Plotly | Interactive scatter, radar, bar charts |
| Visualisation | Seaborn, Matplotlib | Heatmaps, distribution plots |
| Dashboard | Streamlit | Multi-page interactive web app |
| Testing | Pytest, pytest-cov | Unit tests + coverage reporting |
| Linting | Ruff, Black, isort | Code style enforcement |
| Data Format | Parquet (PyArrow) | Efficient columnar storage for processed artifacts |
| Serialisation | Joblib/Pickle | ML model artifact persistence |
| Version Control | Git / GitHub | Source control and CI |

---

## 🔬 Methodology

### Data Pipeline

```
Raw CSV → Validate Schema → Clean (missing values, dedup, type coercion)
→ Engineer Features (per-90, ratios, composites)
→ Log Skewness → RobustScale → KMeans Cluster → Archetype Label
→ Persist Parquet + PKL
```

### Missing Value Strategy

| Column Type | Strategy |
|---|---|
| Critical identifiers (name, club, position) | Row dropped if missing |
| Performance metrics (goals, assists, minutes) | Imputed with `0` (absence = did not occur) |
| Market value | Median imputation grouped by position and age bracket |
| Categorical (nationality, foot) | Imputed with `"Unknown"` |

### Minimum Minutes Threshold

Players with **< 450 minutes** played are excluded from clustering. This corresponds to approximately 5 full matches — the minimum required for per-90 metrics to be statistically stable.

### Why RobustScaler, Not StandardScaler?

K-Means relies on Euclidean distance, which is sensitive to feature scale. `StandardScaler` normalises using mean and standard deviation — but in our dataset, features like `market_value_in_eur` (skewness: **8.74**) and `goals` (skewness: **7.11**) are highly right-skewed with extreme outliers.

`RobustScaler` uses the **median** and **IQR** instead, making the scaling invariant to outliers and producing more balanced cluster shapes.

---

## 📉 Skewness Report & Scaling Decision

The pipeline logs a full skewness report at `logs/skew_report.log`. Key findings:

| Feature | Skewness | Implication |
|---|---|---|
| `international_goals` | 14.56 | Extreme outliers (e.g., Ronaldo/Messi) — `RobustScaler` essential |
| `current_national_team_id` | 38.56 | Excluded from clustering feature set (identity column) |
| `market_value_in_eur` | 8.74 | Excluded from clustering (style ≠ value); used for display only |
| `goals` | 7.11 | Replaced by `goals_per_90` in features; `RobustScaler` applied |
| `red_cards_per_90` | 6.50 | Rare but impactful; robust scaling prevents distortion |
| `goals_per_90` | 1.69 | Acceptable after robust scaling |
| `assists_per_90` | 1.47 | Acceptable after robust scaling |
| `age` | 0.20 | Near-normal — no concern |

> **Deferred to post-v1:** Yeo-Johnson power transforms for features with skewness > 5 in the per-90 space. This would fix distribution *shape* in addition to scale, but adds a second fitted transformer to version and complicates the model artifact. Not required for a defensible v1.

---

## 🧪 Running Tests

```bash
# Run all unit tests
pytest

# Run with coverage report (target ≥ 70% per NFR-09)
pytest --cov=src --cov-report=term-missing

# Run specific test files
pytest tests/test_preprocessing.py tests/test_feature_engineering.py
pytest tests/test_clustering.py tests/test_similarity.py
```

**Test Coverage:**

| Module | Tests | Coverage Target |
|---|---|---|
| `preprocessing.py` | Missing values, dedup, type coercion | ≥ 70% |
| `feature_engineering.py` | Per-90 calculations, min-minutes filter, composite indices | ≥ 70% |
| `clustering.py` | Scaling, KMeans, archetype labelling, K selection | ≥ 70% |
| `similarity.py` | Euclidean distance, top-N ranking | ≥ 70% |
| `dashboard/` | Smoke tests only (UI code excluded from coverage target) | N/A |

---

## ⚠️ Known Limitations

1. **Static Dataset:** The dashboard uses a periodically-refreshed Kaggle snapshot, not live match data. Statistics reflect the last update of the source dataset.
2. **Aggregated Career Stats:** `appearances.csv` is aggregated across all seasons in the dataset. This means a player's cluster reflects their *career* style, not their *current* form.
3. **Limited Defensive Metrics:** The source dataset includes goals, assists, and cards but lacks granular defensive stats (tackles, interceptions, clearances). The Composite Defensive Index is therefore a proxy.
4. **Archetype Labels Are Heuristic:** Cluster names (e.g., "Clinical Finisher") are derived from centroid feature deviations. They represent the *dominant statistical tendency*, not a definitive scouting judgement.
5. **K-Means Assumes Spherical Clusters:** K-Means works best when clusters are roughly convex. Real-world playing styles don't always conform to this assumption. Future versions may explore Gaussian Mixture Models.
6. **Memory Limit:** Streamlit Community Cloud's free tier limits RAM to ~1 GB. The pipeline must be run locally; the deployed app serves only pre-computed artifacts.

---

## 🚀 Future Enhancements

- [ ] Predictive modeling: market value forecasting using supervised learning (XGBoost, LightGBM)
- [ ] Multi-season trend analysis: player development trajectories over time
- [ ] Live data integration via Transfermarkt or StatsBomb API
- [ ] Gaussian Mixture Models / DBSCAN as alternative clustering methods for non-spherical clusters
- [ ] Yeo-Johnson power transforms for highly skewed features (post-v1)
- [ ] Natural-language query interface: *"Show me young left-backs under €10M with high key-passes"* powered by an LLM
- [ ] Automated scouting PDF report generation per player
- [ ] User watchlists and shortlist saving (requires authentication layer)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Data sourced from [Transfermarkt](https://www.transfermarkt.com) via Kaggle ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)).

---

<div align="center">

Built with ❤️ by **AJ-ing** | [GitHub](https://github.com/AJ-ing) | [Live App](https://football-player-performance-playing-style-analytics-dashboard.streamlit.app)

</div>
