# Arquitetura em Nuvem – Google Cloud Platform (GCP)

Este diretório documenta a **arquitetura em nuvem** proposta para suportar o crescimento
do aplicativo **UOLCatLovers**, à medida que o volume de dados e o número de usuários
aumentam significativamente.

A solução foi desenhada considerando **escalabilidade, desacoplamento, baixo custo
operacional, observabilidade e segurança**, utilizando serviços gerenciados da
**Google Cloud Platform (GCP)**.

---

## 🎯 Objetivo da Arquitetura

- Substituir a extração local e armazenamento em CSV por uma solução escalável em nuvem
- Permitir ingestão contínua e resiliente de fatos sobre gatos
- Disponibilizar dados ao aplicativo móvel com **baixa latência**
- Habilitar análises futuras e observabilidade da plataforma

---

## 🧱 Visão Geral da Solução

A arquitetura é composta por cinco camadas principais:

1. **Ingestão de Dados**
2. **Armazenamento**
3. **Processamento / Transformação**
4. **Camada de Disponibilização (Serving)**
5. **Observabilidade e Segurança**

---

## 🔄 Fluxo de Dados

1. O **Cloud Scheduler** dispara execuções periódicas de ingestão
2. O evento é publicado em um tópico do **Pub/Sub**
3. Um **Cloud Run (Ingestion Worker)** consome a mensagem e consulta a **Cat Facts API**
4. Os dados brutos são armazenados no **Cloud Storage (Raw Zone)**
5. Um processo de transformação (Dataflow ou BigQuery SQL) normaliza os dados
6. Os dados processados são:
   - Persistidos no **BigQuery (Curated Zone)** para analytics
   - Disponibilizados em **Firestore** e/ou **Memorystore (Redis)** para serving
7. O aplicativo móvel consome os dados através de uma **API em Cloud Run**, exposta via **API Gateway**

---

## 🗂️ Serviços Utilizados (GCP)

### Ingestão
- **Cloud Scheduler** – Agendamento de execuções
- **Pub/Sub** – Desacoplamento e paralelismo
- **Cloud Run** – Execução do worker de ingestão

### Armazenamento
- **Cloud Storage** – Camada Raw (dados brutos)
- **BigQuery** – Camada Curated (dados analíticos)

### Processamento
- **Dataflow** *ou* **BigQuery SQL** – Transformações e normalização

### Disponibilização
- **Cloud Run (Serving API)** – API para o aplicativo
- **Firestore** – Armazenamento otimizado para leitura
- **Memorystore (Redis)** – Cache de baixa latência
- **API Gateway** – Autenticação, rate limiting e controle de acesso

### Observabilidade e Segurança
- **Cloud Logging**
- **Cloud Monitoring**
- **Secret Manager**
- **IAM (mínimo privilégio)**

---

## 🖼️ Diagrama da Arquitetura

O diagrama abaixo representa visualmente o fluxo descrito:

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