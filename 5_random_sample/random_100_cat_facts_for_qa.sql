-- Query: Random sample of 100 cat facts exported to CSV
-- Database: BigQuery
-- Table: cat_facts_curated
--
-- Objective:
-- Export a random sample of 100 cat facts to a CSV file
-- with comma-separated values for QA environment.

EXPORT DATA OPTIONS (
  uri = 'gs://BUCKET_NAME/qa_exports/cat_facts_sample_*.csv',
  format = 'CSV',
  overwrite = true,
  header = true,
  field_delimiter = ','
) AS
SELECT
  text,
  created_at,
  updated_at
FROM `PROJECT_ID.DATASET_ID.cat_facts_curated`
WHERE text IS NOT NULL
ORDER BY RAND()
LIMIT 100;