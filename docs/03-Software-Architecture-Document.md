# Software Architecture Document (SAD)
## Football Player Performance Analytics Dashboard

---

## Document Control

| Field | Value |
|---|---|
| Document Title | Software Architecture Document — Football Player Performance Analytics Dashboard |
| Version | 1.0 |
| Status | Approved for Development |
| Prepared By | Software Architecture Office, Pitchline Analytics Inc. |
| Date | 11 July 2026 |
| Companion Documents | Software Requirements Document (SRD) v1.0, Technical Requirements Document (TRD) v1.0 |

---

## Executive Summary

This Software Architecture Document (SAD) describes the structural and behavioral design of the Football Player Performance Analytics Dashboard. It presents the system from multiple architectural viewpoints — context, container, component, class, deployment, and behavioral (sequence/activity/state) — using the C4 model as an organizing framework, supplemented with UML-style diagrams rendered in Mermaid. The architecture prioritizes **modularity**, **testability**, and **separation of concerns** between data processing, machine learning, and presentation, enabling the System to evolve (e.g., toward additional leagues, predictive models, or alternative front ends) without wholesale redesign.

---

## 1. Architecture Overview

The System is a **modular monolith**: a single deployable Python application internally organized into well-bounded modules (data, feature engineering, ML/clustering, visualization, presentation) rather than a distributed microservices architecture. This choice reflects the System's scale (single-team, batch-oriented analytics workload, no independent scaling requirements per module) while preserving a clean internal architecture that could be decomposed into services in the future if warranted (see Section 25, Future Expansion Architecture).

---

## 2. Architectural Goals

| Goal | Description |
|---|---|
| Modularity | Clear separation between data, ML, and presentation concerns to enable independent testing and evolution |
| Testability | Business logic (cleaning, feature engineering, clustering) is decoupled from Streamlit UI code and independently unit-testable |
| Reproducibility | Deterministic pipeline outputs given fixed input data and configuration (fixed random seeds for KMeans) |
| Performance | Sub-3-second dashboard load and sub-1-second filter/search response for target dataset scale |
| Maintainability | Consistent module structure, documented interfaces, and a single-responsibility principle applied at the module level |
| Extensibility | New dashboard pages, features, or clustering algorithms can be added without modifying unrelated modules |

---

## 3. Design Principles

- **Separation of Concerns:** Data access, business/ML logic, and presentation are isolated into distinct layers/modules.
- **Single Responsibility Principle:** Each module (`preprocessing.py`, `clustering.py`, etc.) owns exactly one pipeline stage.
- **Don't Repeat Yourself (DRY):** Shared chart-building and formatting logic centralized in `visualization.py` and `utils.py`.
- **Fail Gracefully:** All user-facing errors are caught and translated into actionable messages rather than raw exceptions (see Error Handling Architecture, Section 23).
- **Cache Aggressively, Invalidate Deliberately:** Expensive computations are cached, with explicit cache keys tied to configuration (e.g., K) to avoid stale results.
- **Configuration over Hardcoding:** Paths, thresholds, and clustering parameters are externalized to `config/settings.yaml`.

---

## 4. High-Level Architecture

```mermaid
flowchart TB
    subgraph "Data Layer"
        A1[Raw Dataset\nTransfermarkt/Kaggle CSV]
        A2[Data Loader]
        A3[Preprocessor]
        A4[Feature Engineer]
    end

    subgraph "Analytics / ML Layer"
        B1[Feature Scaler]
        B2[KMeans Clustering Engine]
        B3[Elbow / Silhouette Evaluator]
        B4[Archetype Labeler]
        B5[Similarity Engine]
    end

    subgraph "Presentation Layer"
        C1[Streamlit App Router]
        C2[Dashboard Pages]
        C3[Visualization Engine]
    end

    A1 --> A2 --> A3 --> A4 --> B1 --> B2
    B2 --> B3
    B2 --> B4
    B4 --> B5
    B4 --> C1
    B5 --> C2
    C1 --> C2 --> C3 --> D[User Browser]
```

---

## 5. System Context Diagram

```mermaid
flowchart LR
    User([End User: Analyst / Coach / Student])
    Kaggle[[Kaggle Dataset Source]]
    System[[Football Player Performance\nAnalytics Dashboard]]
    Hosting[(Hosting Platform\nStreamlit Cloud / Docker Host)]

    User -- "Interacts via Browser" --> System
    Kaggle -- "Provides raw CSV dataset\n(periodic manual/CI refresh)" --> System
    System -- "Deployed on" --> Hosting
    System -- "Renders dashboard, accepts filters/search,\nreturns visualizations & exports" --> User
```

**Narrative:** The System sits between an external, periodically-refreshed data source (Kaggle) and end users who interact exclusively through a browser-rendered Streamlit interface. There are no other external system integrations in the current release (no live APIs, no authentication provider, no third-party analytics), keeping the system boundary intentionally narrow.

---

## 6. Container Diagram

```mermaid
flowchart TB
    subgraph "Football Dashboard System"
        direction TB
        Pipeline["Data & ML Pipeline\n(Python module set)\nPreprocessing, Feature Engineering,\nClustering"]
        WebApp["Streamlit Web Application\n(Python / Streamlit)\nMulti-page UI"]
        Store[("File-based Data Store\nParquet / CSV / Pickle")]
    end

    Browser["Web Browser\n(User Client)"]
    RawData[["Raw Kaggle CSV"]]

    RawData --> Pipeline
    Pipeline --> Store
    Store --> WebApp
    WebApp <--> Browser
```

**Container Descriptions:**

| Container | Technology | Responsibility |
|---|---|---|
| Data & ML Pipeline | Python (Pandas, Scikit-learn) | Batch transformation of raw data into a clustered, analysis-ready dataset |
| File-based Data Store | Parquet, CSV, Pickle | Persists intermediate and processed datasets, and serialized ML model artifacts |
| Streamlit Web Application | Python (Streamlit, Plotly) | Serves the interactive multi-page dashboard to end users |

---

## 7. Component Diagram

```mermaid
flowchart TB
    subgraph WebApp[Streamlit Web Application]
        Router[App Router\napp.py]
        Home[Home Page]
        Explorer[Player Explorer Page]
        ClusterPage[Cluster Explorer Page]
        Stats[Statistics Page]
        VizPage[Visual Analytics Page]
        Download[Data Download Page]
        About[About Page]
        Settings[Settings Page]
        VizEngine[Visualization Engine\nvisualization.py]
    end

    subgraph Core[Core Business Logic]
        Loader[data_loader.py]
        Prep[preprocessing.py]
        FE[feature_engineering.py]
        Cluster[clustering.py]
        Sim[similarity.py]
        Utils[utils.py]
        Config[config.py]
    end

    Router --> Home & Explorer & ClusterPage & Stats & VizPage & Download & About & Settings
    Home --> VizEngine
    Explorer --> VizEngine
    Explorer --> Sim
    ClusterPage --> VizEngine
    ClusterPage --> Cluster
    Stats --> VizEngine
    VizPage --> VizEngine
    Download --> Utils

    VizEngine --> Utils
    Loader --> Prep --> FE --> Cluster --> Sim
    Config --> Loader
    Config --> Cluster
    Utils --> Loader
    Utils --> Cluster
```

---

## 8. Module Diagram

```mermaid
flowchart LR
    subgraph src
        config.py
        data_loader.py
        preprocessing.py
        feature_engineering.py
        clustering.py
        similarity.py
        visualization.py
        utils.py
        subgraph dashboard
            home.py
            player_explorer.py
            cluster_explorer.py
            statistics.py
            visual_analytics.py
            data_download.py
            about.py
            settings.py
        end
    end
    app.py --> dashboard
    dashboard --> visualization.py
    dashboard --> similarity.py
    dashboard --> clustering.py
    data_loader.py --> preprocessing.py --> feature_engineering.py --> clustering.py --> similarity.py
    config.py --> data_loader.py
    config.py --> clustering.py
    utils.py --> data_loader.py
    utils.py --> clustering.py
    utils.py --> visualization.py
```

---

## 9. Sequence Diagram

### 9.1 Sequence: Player Search and Comparison

```mermaid
sequenceDiagram
    actor U as User
    participant App as App Router
    participant PE as Player Explorer Page
    participant Cache as Session Cache
    participant Sim as Similarity Engine
    participant Viz as Visualization Engine

    U->>App: Navigate to "Player Explorer"
    App->>PE: render()
    PE->>Cache: get_processed_dataset()
    Cache-->>PE: cluster-labeled DataFrame
    U->>PE: Enter search text "Kane"
    PE->>PE: filter_dataframe(name contains "Kane")
    PE-->>U: Display matching players table
    U->>PE: Select two players, click "Compare"
    PE->>Viz: build_radar_chart(player_a, player_b, metrics)
    Viz-->>PE: Plotly Figure
    PE-->>U: Render radar chart + comparison table
    U->>PE: Click "Find Similar Players"
    PE->>Sim: find_similar(player_id, top_n=5)
    Sim-->>PE: Ranked similar players list
    PE-->>U: Display similar players
```

### 9.2 Sequence: Data Pipeline Execution (Startup / Cache Miss)

```mermaid
sequenceDiagram
    participant App as Streamlit App
    participant Loader as data_loader.py
    participant Prep as preprocessing.py
    participant FE as feature_engineering.py
    participant Clus as clustering.py
    participant Store as File-based Data Store

    App->>Loader: load_dataset(config.data.raw_path)
    Loader->>Store: read CSV
    Store-->>Loader: raw DataFrame
    Loader-->>App: raw DataFrame (validated)
    App->>Prep: clean(raw_df)
    Prep-->>App: cleaned DataFrame
    App->>FE: engineer_features(cleaned_df)
    FE-->>App: feature DataFrame
    App->>Clus: fit_and_predict(feature_df, k=default_k)
    Clus->>Clus: StandardScaler.fit_transform()
    Clus->>Clus: KMeans.fit_predict()
    Clus->>Store: persist model.pkl
    Clus-->>App: cluster-labeled DataFrame
    App->>App: st.cache_data.set(result)
```

---

## 10. Activity Diagram

### 10.1 Activity: End-to-End Data Processing

```mermaid
flowchart TD
    Start([Start]) --> Load[Load Raw CSV]
    Load --> Valid{Schema Valid?}
    Valid -- No --> ErrLog[Log Error &\nRaise DataValidationError]
    ErrLog --> ErrUI[Display Error Banner in UI]
    ErrUI --> End1([End])
    Valid -- Yes --> Clean[Clean & Normalize Data]
    Clean --> Engineer[Engineer Derived Features]
    Engineer --> Scale[Standardize Features]
    Scale --> Cluster[Fit KMeans / Predict Clusters]
    Cluster --> Label[Assign Archetype Labels]
    Label --> Persist[Persist Processed Dataset\n& Model Artifacts]
    Persist --> Cache[Populate Streamlit Cache]
    Cache --> Ready([Dashboard Ready for User Interaction])
```

---

## 11. Data Flow Diagram

```mermaid
flowchart LR
    RawCSV[(Raw CSV)] --> P1((Load & Validate))
    P1 --> P2((Clean))
    P2 --> P3((Engineer Features))
    P3 --> P4((Scale))
    P4 --> P5((Cluster))
    P5 --> DS1[(Processed Dataset)]
    P5 --> DS2[(Model Artifact)]
    DS1 --> P6((Filter / Search))
    P6 --> P7((Visualize))
    P7 --> UserOut([User: Charts, Tables, KPIs])
    DS1 --> P8((Similarity Query))
    P8 --> UserOut
    DS1 --> P9((Export))
    P9 --> FileOut([Downloaded CSV])
```

---

## 12. Class Diagram

```mermaid
classDiagram
    class Config {
        +str data_raw_path
        +int default_k
        +int min_minutes_threshold
        +str log_level
        +load() Config
    }

    class DataLoader {
        +load_dataset(path str) DataFrame
        -validate_schema(df DataFrame) None
    }

    class Preprocessor {
        +clean(df DataFrame) DataFrame
        -handle_missing_values(df DataFrame) DataFrame
        -deduplicate(df DataFrame) DataFrame
        -normalize_categoricals(df DataFrame) DataFrame
    }

    class FeatureEngineer {
        +engineer_features(df DataFrame) DataFrame
        -per_90(df DataFrame, col str) Series
        -composite_index(df DataFrame, weights dict) Series
    }

    class ClusteringEngine {
        -scaler StandardScaler
        -model KMeans
        +fit_predict(df DataFrame, k int) DataFrame
        +evaluate_k(df DataFrame, k_range range) dict
        +label_archetypes(centroids ndarray) list
        +save(path str) None
        +load(path str) ClusteringEngine
    }

    class SimilarityEngine {
        +find_similar(player_id str, top_n int) list
        -compute_distance(vec_a ndarray, vec_b ndarray) float
    }

    class VisualizationEngine {
        +build_scatter(df DataFrame) Figure
        +build_radar(players list, metrics list) Figure
        +build_heatmap(df DataFrame) Figure
        +build_elbow_chart(k_scores dict) Figure
    }

    class DashboardPage {
        <<interface>>
        +render(state SessionState) None
    }

    class PlayerExplorerPage {
        +render(state SessionState) None
    }

    class ClusterExplorerPage {
        +render(state SessionState) None
    }

    DataLoader --> Preprocessor
    Preprocessor --> FeatureEngineer
    FeatureEngineer --> ClusteringEngine
    ClusteringEngine --> SimilarityEngine
    DashboardPage <|.. PlayerExplorerPage
    DashboardPage <|.. ClusterExplorerPage
    PlayerExplorerPage --> SimilarityEngine
    PlayerExplorerPage --> VisualizationEngine
    ClusterExplorerPage --> ClusteringEngine
    ClusterExplorerPage --> VisualizationEngine
    Config --> DataLoader
    Config --> ClusteringEngine
```

---

## 13. Deployment Diagram

```mermaid
flowchart TB
    subgraph "Developer Machine"
        Git[Git Repository]
    end

    subgraph "CI/CD: GitHub Actions"
        Lint[Lint Job]
        Test[Test Job]
        Build[Build Docker Image]
    end

    subgraph "Hosting Environment"
        subgraph "Container / Streamlit Cloud Instance"
            App[Streamlit App Process]
            Data[(Mounted / Bundled\nData Volume)]
        end
    end

    Browser[User Web Browser]

    Git -->|push / PR| Lint --> Test --> Build
    Build -->|deploy| App
    Data --> App
    Browser <-->|HTTPS :443 -> :8501| App
```

**Deployment Notes:** The application is packaged as a single container image containing the Python runtime, application code, and (optionally) a pre-processed data snapshot baked into the image or mounted as a volume. Streamlit listens on port 8501 internally, fronted by the hosting platform's HTTPS termination (Streamlit Community Cloud) or a reverse proxy/load balancer (self-hosted container deployment).

---

## 14. State Diagram

### 14.1 State: Dashboard Session Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> LoadingData: App starts
    LoadingData --> DataError: Load/Validation fails
    LoadingData --> Ready: Load succeeds (cache populated)
    DataError --> [*]: User sees error, session ends or retries
    Ready --> Browsing: User navigates pages
    Browsing --> Filtering: User applies search/filters
    Filtering --> Browsing: Results rendered
    Browsing --> Comparing: User selects players
    Comparing --> Browsing: Comparison rendered
    Browsing --> Reclustering: User changes K (Settings)
    Reclustering --> Ready: New cluster labels cached
    Browsing --> Exporting: User requests export
    Exporting --> Browsing: File downloaded
    Browsing --> [*]: Session ends
```

---

## 15. Package Diagram

```mermaid
flowchart TB
    subgraph pkg_app["package: app"]
        app_py[app.py]
    end
    subgraph pkg_dashboard["package: src.dashboard"]
        dp[Dashboard Page Modules]
    end
    subgraph pkg_core["package: src.core (business logic)"]
        core[data_loader, preprocessing,\nfeature_engineering, clustering, similarity]
    end
    subgraph pkg_viz["package: src.visualization"]
        viz[visualization.py]
    end
    subgraph pkg_common["package: src.common"]
        common[config.py, utils.py]
    end

    pkg_app --> pkg_dashboard
    pkg_dashboard --> pkg_viz
    pkg_dashboard --> pkg_core
    pkg_core --> pkg_common
    pkg_viz --> pkg_common
```

**Dependency Rule:** Packages depend only "inward" toward `src.common`; `src.core` has no dependency on `src.dashboard` or Streamlit itself, which is what makes the business logic independently unit-testable (see TRD Section 18, Testing Strategy).

---

## 16. Layered Architecture

```mermaid
flowchart TB
    L1["Presentation Layer\n(Streamlit pages, widgets, navigation)"]
    L2["Application / Orchestration Layer\n(page-level controllers calling core services)"]
    L3["Domain / Business Logic Layer\n(preprocessing, feature engineering, clustering, similarity)"]
    L4["Data Access Layer\n(data_loader, file I/O, model persistence)"]
    L5["Infrastructure Layer\n(config, logging, caching utilities)"]

    L1 --> L2 --> L3 --> L4 --> L5
    L1 -.uses.-> L5
    L3 -.uses.-> L5
```

| Layer | Responsibility | Example Modules |
|---|---|---|
| Presentation | Render UI, capture user input | `dashboard/*.py`, `app.py` |
| Application/Orchestration | Coordinate calls to domain services per page action | Page-level render functions |
| Domain/Business Logic | Core analytics/ML rules, independent of UI framework | `preprocessing.py`, `feature_engineering.py`, `clustering.py`, `similarity.py` |
| Data Access | Read/write raw, interim, processed data, and model artifacts | `data_loader.py`, model save/load routines |
| Infrastructure | Cross-cutting concerns | `config.py`, `utils.py`, logging setup |

---

## 17. MVC / MVVM Discussion

Streamlit does not natively enforce an MVC/MVVM pattern, as it re-executes the script top-to-bottom on each interaction and blends view and controller concerns within page functions. The System approximates a pragmatic **Model-View-Controller-like separation**:

- **Model:** `src/` core business-logic modules (`preprocessing.py`, `feature_engineering.py`, `clustering.py`, `similarity.py`) plus the processed `DataFrame`/model artifacts — entirely independent of Streamlit.
- **View:** Widget composition and layout code within `dashboard/*.py` (calls to `st.dataframe`, `st.plotly_chart`, `st.selectbox`, etc.).
- **Controller:** The thin orchestration logic within each page's `render()` function that interprets `st.session_state` and user widget events, invokes Model functions, and passes results to View rendering calls.

This separation is enforced by convention and code review rather than framework mechanics, and is validated by the constraint that all Model modules must be importable and testable without importing Streamlit.

---

## 18. Architectural Decisions

### ADR-01: Modular Monolith over Microservices
**Decision:** Implement as a single deployable modular Python application.
**Rationale:** The workload is single-tenant, batch-oriented, and does not require independent scaling of components. Microservices would add operational overhead disproportionate to project scale.
**Status:** Accepted.

### ADR-02: File-based Storage over Relational Database
**Decision:** Use Parquet/CSV/Pickle file storage rather than a database engine.
**Rationale:** Read-heavy, single-writer batch pipeline; no concurrent transactional writes; minimizes infrastructure dependencies for a portfolio/academic deployment target.
**Status:** Accepted; revisit if multi-user persistence (watchlists, accounts) is introduced.

### ADR-03: K-Means as Primary Clustering Algorithm
**Decision:** Use K-Means as the primary unsupervised clustering method, with Elbow Method and Silhouette Score for K selection.
**Rationale:** K-Means is computationally efficient, well-understood, and produces interpretable centroid-based archetypes suitable for the target audience. Alternative algorithms (DBSCAN, Gaussian Mixture Models) are noted as future enhancements where cluster shapes are non-spherical or density-based grouping is desired.
**Status:** Accepted.

### ADR-04: Streamlit over Custom Web Framework
**Decision:** Use Streamlit rather than a custom Flask/React application.
**Rationale:** Streamlit enables rapid development of data-centric interactive dashboards with minimal front-end engineering overhead, aligning with project scope and timeline.
**Status:** Accepted; trade-off is reduced UI customization flexibility relative to a bespoke front end.

### ADR-05: Exclude Market Value from Clustering Feature Set
**Decision:** Clustering features are restricted to on-pitch performance metrics; market value and wage are excluded from the feature set used for K-Means.
**Rationale:** Including market value would bias clusters toward "expensive vs. cheap" rather than "playing style," undermining the System's core value proposition of style-based archetype discovery.
**Status:** Accepted.

---

## 19. Design Patterns Used

| Pattern | Application |
|---|---|
| **Pipeline Pattern** | Sequential data transformation stages (load → clean → engineer → scale → cluster) |
| **Repository Pattern (lightweight)** | `data_loader.py` abstracts the source of data, enabling future substitution (e.g., database or API source) without changing downstream modules |
| **Strategy Pattern** | Archetype-labeling heuristics and missing-value imputation strategies are configurable per feature/column |
| **Facade Pattern** | `visualization.py` provides a simplified interface over Plotly/Matplotlib/Seaborn for dashboard pages |
| **Singleton-like Caching** | `st.cache_resource` ensures a single fitted clustering model instance is reused across a session |
| **Template Method (implicit)** | Each `dashboard/*.py` page follows a consistent `render(state)` structure |

---

## 20. Scalability Considerations

- **Vertical scaling** (increased host memory/CPU) is the primary scaling lever for the current file-based, in-memory Pandas architecture.
- For datasets significantly larger than tens of thousands of rows, migration to a columnar analytical engine (e.g., DuckDB or Polars) is recommended to avoid full in-memory Pandas materialization on every session.
- The layered architecture (Section 16) permits horizontal decomposition into services (e.g., a separate clustering microservice) in the future without rewriting domain logic, since domain modules have no direct dependency on the Streamlit process.
- Caching (`st.cache_data`, `st.cache_resource`) reduces repeated computation load as concurrent user sessions increase.

---

## 21. Maintainability Considerations

- Strict module boundaries and the dependency rule in Section 15 (Package Diagram) prevent circular dependencies and keep business logic UI-agnostic.
- Consistent docstring conventions (NFR-10 in the SRD) and type hints improve onboarding and IDE tooling support.
- A dedicated `tests/` suite mirroring `src/` structure ensures regressions are caught early (see TRD Section 18).
- Configuration externalization (Section 15, TRD) avoids scattering "magic numbers" (e.g., default K, minimum minutes threshold) throughout the codebase.

---

## 22. Security Architecture

- The System operates on public, non-sensitive statistical data; no PII is processed (see SRD FR-25, NFR-06/07).
- Export sanitization mitigates CSV formula injection (TRD Section 20).
- No arbitrary code execution paths are exposed to end users; all filtering and querying use parameterized Pandas operations.
- Dependency vulnerability scanning is integrated into CI (TRD Section 20).
- Since there is no authentication layer in the current release, the System assumes a trusted, read-only, single-tenant deployment; introducing multi-user accounts in the future (SRD Section 21, Future Enhancements) would require a dedicated identity/authorization architecture, out of scope for this release.

---

## 23. Error Handling Architecture

```mermaid
flowchart TD
    Err[Exception Raised in Core Module] --> Catch{Caught by\nPage-level Boundary?}
    Catch -- Yes --> Classify{Known AppError\nSubtype?}
    Classify -- Yes --> Friendly[Render Friendly,\nActionable Message]
    Classify -- No --> Generic[Render Generic\n'Something went wrong' Message]
    Catch -- No --> Propagate[Propagate to Streamlit\nDefault Error Handler]
    Friendly --> LogErr[Log Full Stack Trace\nat ERROR level]
    Generic --> LogErr
    Propagate --> LogErr
```

All custom exceptions inherit from a common `AppError` base class (see TRD Section 17), enabling a single `try/except AppError` boundary within each page's `render()` function. This ensures users never see raw Python tracebacks, satisfying NFR-04 (Reliability) and FR-21 (Error Handling) from the SRD.

---

## 24. Performance Architecture

- **Cache-first data access:** All page render functions retrieve data via cached accessor functions rather than re-reading files or re-running the pipeline.
- **Vectorized transformations:** No row-wise Python iteration in the hot path of preprocessing or feature engineering.
- **Lazy computation:** Visualizations are computed only for the currently active page, not pre-rendered for all pages on every rerun.
- **Bounded result rendering:** Tables are paginated to avoid rendering excessively large DOM structures in the browser.
- **Model reuse:** The fitted KMeans model and scaler are cached as a resource, avoiding repeated fitting on every user interaction (fitting only occurs on initial load or explicit K change).

---

## 25. Future Expansion Architecture

Should the System's scope grow (e.g., multi-league support, predictive modeling, user accounts, or real-time data), the following expansion path is architecturally supported by the current layered, modular design:

```mermaid
flowchart LR
    subgraph "Current Architecture"
        Mono[Modular Monolith\nData + ML + Presentation]
    end

    subgraph "Potential Future Architecture"
        API[Analytics API Service\n(FastAPI)]
        MLSvc[ML/Clustering Service]
        DB[(Managed Database\nPostgreSQL)]
        Auth[Auth Service]
        FE2[Front End\n(Streamlit or React SPA)]
    end

    Mono -.evolves into.-> API
    Mono -.evolves into.-> MLSvc
    API --> DB
    MLSvc --> DB
    Auth --> API
    FE2 --> API
```

Because domain logic (`src/core`) has no dependency on the Streamlit presentation layer (enforced by the Package Diagram's dependency rule), extracting `clustering.py` and `similarity.py` into an independent service, or replacing the Streamlit front end with a different client, would require changes only at the integration boundary, not within the domain logic itself.

---

*End of Software Architecture Document.*
