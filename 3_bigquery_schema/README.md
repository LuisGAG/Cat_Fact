# 3) BigQuery – Esquema da Tabela (Cat Facts)

Esta etapa descreve o **esquema da tabela no BigQuery** para armazenamento e consulta
dos fatos sobre gatos (cat facts) pelo time de Analytics.

A proposta abaixo representa uma tabela **curated** (camada tratada), adequada para:
- consultas SQL ad-hoc
- dashboards/BI
- governança mínima (linhagem e rastreabilidade)

---

## 🎯 Objetivo

- Padronizar os campos da API em uma tabela única no BigQuery
- Permitir consultas rápidas, com particionamento e clusterização
- Garantir deduplicação por chave natural do fato (`fact_id`)
- Manter metadados de ingestão para auditoria e troubleshooting

---

## 🧱 Tabela Proposta: `cat_facts_curated`

Arquivo SQL: `cat_facts_table.sql`

### Campos (resumo)

**Chave**
- `fact_id` (STRING, NOT NULL): identificador do fato no sistema de origem (`_id`/`id`)

**Conteúdo**
- `text` (STRING): texto do fato
- `fact_type` (STRING): tipo/categoria (quando existir)
- `source` (STRING): origem do fato (quando existir)
- `used` (BOOL): flag de uso (quando existir)
- `deleted` (BOOL): flag de exclusão (quando existir)

**Status**
- `status_verified` (BOOL): verificado (quando existir)
- `status_sent_count` (INT64): contador de envio (quando existir)

**Usuário**
- `user_id` (STRING): id do usuário associado (quando existir)
- `user_name` (STRING): nome do usuário (quando existir)

**Timestamps da origem**
- `created_at` (TIMESTAMP): data/hora de criação do fato na origem (quando existir)
- `updated_at` (TIMESTAMP): data/hora de atualização na origem (quando existir)

**Metadados de ingestão**
- `api_source` (STRING, NOT NULL): origem do dado (ex.: `cat-fact.herokuapp.com`)
- `ingested_at` (TIMESTAMP, NOT NULL): data/hora da coleta em UTC
- `load_date` (DATE, NOT NULL): coluna usada para particionamento (derivada de `ingested_at`)
- `raw_payload` (JSON, opcional): payload bruto (auditoria). Em escala muito grande, preferir armazenar raw em GCS.

---

## 🧩 Considerações importantes

### Particionamento
- **PARTITION BY `load_date`**
  - reduz custo de consulta ao filtrar por data
  - facilita retenção/expurgo por partição

### Clusterização
- **CLUSTER BY `fact_id`, `status_verified`**
  - acelera buscas por id e filtros comuns
  - ajuda na performance em grandes volumes

### Deduplicação (recomendação)
Como `fact_id` vem da origem, a deduplicação pode ser feita com uma estratégia de upsert:
- manter a linha mais recente por `fact_id` usando `updated_at` ou `ingested_at`
- implementar via `MERGE` em uma tabela final

### Tipos e parsing
- Campos de data/hora da origem podem vir em string ISO.
  - converter para TIMESTAMP no processo de carga/transformação.

---

## ✅ Exemplo de consulta típica (Analytics)

```sql
SELECT
  load_date,
  COUNT(*) AS facts_ingested,
  COUNTIF(status_verified) AS verified_facts
FROM `PROJECT_ID.DATASET_ID.cat_facts_curated`
WHERE load_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY load_date
ORDER BY load_date;
```

## 🧩 Modelo de Dados – Cat Facts (BigQuery)

```mermaid
erDiagram
  CAT_FACTS_CURATED {
    STRING fact_id PK
    STRING text
    STRING fact_type
    STRING source
    BOOL used
    BOOL deleted

    BOOL status_verified
    INT64 status_sent_count

    STRING user_id
    STRING user_name

    TIMESTAMP created_at
    TIMESTAMP updated_at

    STRING api_source
    TIMESTAMP ingested_at
    DATE load_date
    JSON raw_payload
  }
  ```