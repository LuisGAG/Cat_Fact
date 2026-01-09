-- BigQuery table schema for Cat Facts (curated layer)
-- Recommended: create in a dataset like `uolcatlovers_analytics`

CREATE TABLE IF NOT EXISTS `PROJECT_ID.DATASET_ID.cat_facts_curated`
(
  -- Business key / natural key from the source API
  fact_id STRING NOT NULL,                 -- source: _id / id

  -- Fact content
  text STRING,                             -- source: text / fact
  fact_type STRING,                        -- source: type (when available)
  source STRING,                           -- source: source (when available)
  used BOOL,                               -- source: used (when available)
  deleted BOOL,                            -- source: deleted (when available)

  -- Status object (when available)
  status_verified BOOL,                    -- source: status.verified
  status_sent_count INT64,                 -- source: status.sentCount

  -- User object (when available)
  user_id STRING,                          -- source: user._id
  user_name STRING,                        -- source: user.name (string or derived from {first,last})

  -- Timestamps from source (may be null depending on API payload)
  created_at TIMESTAMP,                    -- source: createdAt
  updated_at TIMESTAMP,                    -- source: updatedAt

  -- Ingestion / lineage metadata
  api_source STRING NOT NULL,              -- e.g. "cat-fact.herokuapp.com" or "catfact.ninja"
  ingested_at TIMESTAMP NOT NULL,          -- ingestion time (UTC)
  load_date DATE NOT NULL,                 -- date partition column, derived from ingested_at

  -- Optional: raw payload for auditing/debug (keep small or store in GCS for large payloads)
  raw_payload JSON                         -- original event as JSON (optional)
)
PARTITION BY load_date
CLUSTER BY fact_id, status_verified;