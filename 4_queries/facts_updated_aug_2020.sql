-- Query: Cat facts updated in August 2020
-- Database: BigQuery
-- Table: cat_facts_curated
--
-- Objective:
-- Extract all cat facts that were updated during August 2020
-- to support an analytics study case.

SELECT
  *
FROM `PROJECT_ID.DATASET_ID.cat_facts_curated`
WHERE updated_at IS NOT NULL
  AND updated_at >= TIMESTAMP('2020-08-01')
  AND updated_at <  TIMESTAMP('2020-09-01');