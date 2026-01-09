# 5) Amostragem Aleatória – BigQuery (QA)

Este diretório contém a consulta SQL solicitada pelo time de desenvolvimento
para **extrair uma amostra aleatória de fatos sobre gatos** e popular o ambiente de QA.

Conforme a nota do desafio, **não é necessária a execução da consulta**, apenas
a definição do código SQL.

---

## 📌 Consulta: Amostra aleatória de 100 registros

Arquivo: `random_100_cat_facts_for_qa.sql`

### Campos retornados
- `text` – texto do fato
- `created_at` – data de criação na origem
- `updated_at` – data de última atualização na origem

### Estratégia adotada
- `ORDER BY RAND()` para aleatoriedade
- `LIMIT 100` para controle do tamanho da amostra
- Exclusão de registros com texto nulo

---

### Exportação para CSV

A consulta utiliza o comando `EXPORT DATA` do BigQuery,
que permite exportar diretamente o resultado da query
para arquivos CSV separados por vírgulas em um bucket
do Google Cloud Storage.