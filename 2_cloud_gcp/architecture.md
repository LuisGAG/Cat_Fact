```mermaid
flowchart LR
  A["Mobile App"] -->|HTTPS| AGW["API Gateway"]
  AGW --> API["Cloud Run - Serving API"]

  API --> R["Memorystore Redis - cache"]
  API --> FS["Firestore - serving store"]
  API --> BQ["BigQuery - Curated"]

  subgraph Ingestion
    SCH["Cloud Scheduler"]
    PS["Pub/Sub Topic"]
    CRJ["Cloud Run - Ingestion Worker"]
    EXT["Cat Facts API"]
    GCS["Cloud Storage - Raw Zone"]

    SCH --> PS
    PS --> CRJ
    CRJ --> EXT
    CRJ --> GCS
  end

  subgraph Processing
    DF["Dataflow / BigQuery SQL Transform"]
    GCS --> DF
    DF --> BQ
    DF --> FS
    DF --> R
  end

  subgraph Observability_and_Security["Observability & Security"]
    LOG["Cloud Logging"]
    MON["Cloud Monitoring"]
    SM["Secret Manager"]
  end

  CRJ --> LOG
  API --> LOG
  LOG --> MON
  CRJ --> SM
  API --> SM