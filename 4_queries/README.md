# 4) Consultas Analíticas – BigQuery

Este diretório contém consultas SQL desenvolvidas para auxiliar o
time de Analytics no uso dos dados de **cat facts** armazenados no BigQuery.

Conforme solicitado no desafio, **não é necessária a execução das consultas**,
apenas a definição do código SQL.

---

## 📌 Consulta: Fatos atualizados em agosto de 2020

Arquivo: `facts_updated_aug_2020.sql`

### Descrição
Extrai todos os fatos sobre gatos que foram **atualizados durante o mês de agosto de 2020**,
com base no campo `updated_at`.

### Estratégia adotada
- Filtro por intervalo de datas (`>=` início do mês e `<` início do mês seguinte)
- Exclusão de registros com `updated_at` nulo
- Compatível com tabelas grandes e particionadas

### Exemplo de uso
```sql
SELECT
  *
FROM `PROJECT_ID.DATASET_ID.cat_facts_curated`
WHERE updated_at >= TIMESTAMP('2020-08-01')
  AND updated_at <  TIMESTAMP('2020-09-01');