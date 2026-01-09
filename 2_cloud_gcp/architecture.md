```mermaid
flowchart LR
  A[Mobile App] -->|HTTPS| AGW[API Gateway]
  AGW --> API[Cloud Run - Serving API]

  API --> R[Memorystore Redis (cache)]
  API --> FS[Firestore (serving store)]
  API -->|optional analytics| BQ[(BigQuery Curated)]

  subgraph Ingestion
    SCH[Cloud Scheduler] --> PS[(Pub/Sub Topic)]
    PS --> CRJ[Cloud Run - Ingestion Worker]
    CRJ --> EXT[Cat Facts API]
    CRJ --> GCS[(Cloud Storage - Raw Zone)]
  end

  subgraph Processing
    GCS --> DF[Dataflow / BQ SQL Transform]
    DF --> BQ
    DF --> FS
    DF --> R
  end

  subgraph Observability & Security
    LOG[Cloud Logging]
    MON[Cloud Monitoring]
    SM[Secret Manager]
  end

  CRJ --> LOG
  API --> LOG
  LOG --> MON
  CRJ --> SM
  API --> SM