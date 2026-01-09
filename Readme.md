# Cat_Fact – UOLCatLovers Data Engineering Challenge

Este repositório contém a solução completa para o desafio técnico proposto pela startup
fictícia **UOLCatLovers**, cujo objetivo é coletar, armazenar, escalar e disponibilizar
fatos interessantes sobre gatos (cat facts) a partir da **Cat Facts API**.

Documentação da API utilizada:
https://alexwohlbruck.github.io/cat-facts/docs/

A solução foi estruturada em **etapas evolutivas**, refletindo o crescimento do produto
e as diferentes necessidades dos times envolvidos (engenharia, analytics e desenvolvimento).

---

## 📁 Estrutura do Repositório

Cat_Fact/
│
├─ 1_local/
├─ 2_cloud_gcp/
├─ 3_bigquery_schema/
├─ 4_queries/
├─ 5_random_sample/
└─ README.md


Cada pasta corresponde diretamente a **um item do desafio**.

---

## 1️⃣ Solução Local – Extração para CSV

📂 **Pasta:** `1_local/`

**Objetivo:**  
Desenvolver um script Python simples que consuma a Cat Facts API e salve os dados localmente
em um arquivo CSV, adequado para um cenário inicial de baixo volume.

**Conteúdo:**
- Script Python para extração dos dados
- Salvamento local em CSV
- Arquivo `requirements.txt`
- README com instruções de execução

Essa etapa atende ao **Item 1 do desafio**.

---

## 2️⃣ Arquitetura em Nuvem – Google Cloud Platform

📂 **Pasta:** `2_cloud_gcp/`

**Objetivo:**  
Projetar uma arquitetura escalável em **Google Cloud Platform (GCP)** para suportar o
crescimento exponencial do volume de dados e usuários do aplicativo.

**Conteúdo:**
- Descrição da arquitetura proposta
- Diagrama em Mermaid renderizado no GitHub
- Explicação do fluxo de ingestão, armazenamento, processamento e serving
- Considerações de escalabilidade, segurança e observabilidade

Não há código nesta etapa, apenas **desenho e documentação**, conforme solicitado.

Essa etapa atende ao **Item 2 do desafio**.

---

## 3️⃣ Esquema de Dados – BigQuery

📂 **Pasta:** `3_bigquery_schema/`

**Objetivo:**  
Especificar o esquema da tabela de fatos sobre gatos no **BigQuery**, permitindo que o time
de Analytics realize consultas de forma independente.

**Conteúdo:**
- Definição completa do esquema da tabela `cat_facts_curated`
- Tipos de dados, chaves e metadados de ingestão
- Considerações sobre particionamento, clusterização e deduplicação
- Diagrama do esquema da tabela (Mermaid)
- Arquivo SQL com a definição da tabela

Essa etapa atende ao **Item 3 do desafio**.

---

## 4️⃣ Consulta Analítica – Atualizações em Agosto de 2020

📂 **Pasta:** `4_queries/`

**Objetivo:**  
Auxiliar o time de Analytics com uma consulta SQL que extraia todos os fatos que foram
**atualizados durante o mês de agosto de 2020**.

**Conteúdo:**
- Consulta SQL em BigQuery
- Filtro temporal adequado (`updated_at`)
- README explicando a estratégia adotada

Conforme a nota do desafio, não é necessária a execução da consulta.

Essa etapa atende ao **Item 4 do desafio**.

---

## 5️⃣ Amostragem Aleatória – Exportação para CSV (QA)

📂 **Pasta:** `5_random_sample/`

**Objetivo:**  
Fornecer ao time de desenvolvimento uma consulta SQL que gere uma **amostra aleatória
de 100 registros** da base de cat facts para popular o ambiente de QA, com exportação
direta para **CSV separado por vírgulas**.

**Conteúdo:**
- Consulta SQL utilizando `EXPORT DATA`
- Seleção dos campos: texto, data de criação e data de atualização
- Exportação para CSV no Google Cloud Storage
- README explicando o propósito da consulta

Essa etapa atende ao **Item 5 do desafio**.

---

## ✅ Considerações Finais

- Todas as entregas estão organizadas em um único repositório GitHub
- Cada pasta corresponde claramente a um item do desafio
- O projeto demonstra evolução de uma solução local simples para uma arquitetura escalável
- O foco está em clareza, boas práticas e comunicação técnica

Este repositório foi estruturado para facilitar a leitura, avaliação e entendimento
do raciocínio aplicado em cada etapa do desafio.