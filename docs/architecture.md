# CryptoTrace Architecture & System Specification

CryptoTrace is a real-time crypto fraud attribution system built for Smart India Hackathon 2026 (SIH26183, Team 404BoysNotFounds). It takes victim-reported crypto wallets (from NCRP / SAHYOG), traces fund movement across multiple hops and EVM chains, attributes target wallets/VASPs, scores risk using an ML ensemble, and generates court-ready dossier reports backed by an immutable Merkle audit log.

---

## 1. System Layers

| Layer | Components | Technology Stack |
| :--- | :--- | :--- |
| **Presentation** | Investigator dashboard, review queue, alerts, audit log, SAHYOG mock portal | Next.js 14 (App Router, TypeScript), Tailwind CSS, TanStack Query, Cytoscape.js, Recharts |
| **API Gateway** | REST API + SSE, JWT authentication, Casbin RBAC, rate limiting (`slowapi`), `/metrics` | FastAPI, Pydantic v2, PyJWT, Casbin, Prometheus instrumentator |
| **Orchestration** | Celery worker nodes (1 task per stage), event emission via Redis pub/sub, Celery beat | Celery 5, Redis 7 |
| **Analytics Core** | Graph tracing (APPR), clustering, heuristic attribution, cross-chain bridge matching, risk scoring | NetworkX, NumPy, pandas, XGBoost, scikit-learn, SHAP |
| **Data Layer** | Case metadata & audit log (Postgres/Supabase), graph store (Neo4j), cache/queues (Redis), evidence PDFs (MinIO) | PostgreSQL 16, Neo4j 5, Redis 7, MinIO S3 |
| **Chain Ingestion** | Chain provider abstraction: Alchemy primary, Etherscan fallback, fixture provider for tests | `httpx`, `tenacity` |
| **Edge / Ops** | Docker Compose, Caddy (TLS 1.3 edge), Prometheus, Grafana, MLflow | Docker, Caddy, Prometheus, Grafana, MLflow |

---

## 2. The 8-Stage Pipeline

```
NCRP/SAHYOG --(signed POST)--> [1 INGEST] create case, validate address, SHA-256 anchor (Himanshi)
                                 | Celery: run_case(case_id)
                                 v
                               [2 TRACE] TraceRequest -> TraceGraph (Tanisha)
                                 v
                               [3 CLUSTER] TraceGraph -> list[EntityCluster] (Tanisha)
                                 v
                               [4 ATTRIBUTE] graph+clusters+labels -> list[Attribution] (Monica)
                                 v
                               [5 CROSSCHAIN] graph -> list[CrossChainLink] (Kanak)
                                 v
                               [6 RISK] addresses -> list[RiskScore] (+SHAP) (Sristhi)
                                 v
                               [7 REPORT] dossier PDF + hash list + freeze template (Kanak)
                                 v
                               [8 DELIVER] dashboard update, SAHYOG webhook, audit entry (Himanshi)
```

Every stage execution:
1. Emits a `PipelineEvent` to Redis channel `ct:case:{case_id}`.
2. Writes an artifact JSON to MinIO evidence store.
3. Computes the SHA-256 hash of the artifact.
4. Appends a record to the tamper-evident Merkle audit log.

---

## 3. Core Architectural Rules

1. **Protocol-Driven Core Engines**:
   All core engines (`app/engines/*`) implement standard Python `Protocol` interfaces defined in `app/engines/base.py`. They are pure domain functions completely decoupled from HTTP, Celery, database connections, and external API keys. Input and output objects are strictly validated Pydantic models from `app/contracts/`.

2. **Universal Fixture Support**:
   Setting `CT_PROVIDER=fixture` enables offline mode where all chain data is loaded deterministically from `tests/fixtures/demo_case_001/`. The entire API, pipeline, and UI operate seamlessly with zero external API dependencies.

3. **Two-Number Attribution Rule**:
   - `hop_distance` & `proximity_rank`: Answer *how close* the target wallet is to a known VASP.
   - `confidence` & `evidence_tier`: Answer *how credible* the attribution is.
   - These numbers are never averaged or blended together.

---

## 4. PPT Traceability Matrix

| PPT Claim | Stage / Feature | Owner | Implementation Path |
| :--- | :--- | :--- | :--- |
| SAHYOG/NCRP Ingest | Ingest | Himanshi | `backend/app/integrations/sahyog_mock.py`, `api/v1/ingest.py` |
| Stage 1 Ingestion | Ingest | Himanshi | `backend/app/api/v1/ingest.py`, `app/audit/evidence.py` |
| Stage 2 Tracing | Tracing | Tanisha | `backend/app/engines/tracing/` |
| Stage 3 Clustering | Clustering | Tanisha | `backend/app/engines/clustering/` |
| Stage 4 Attribution | Attribution | Monica | `backend/app/engines/attribution/` |
| Stage 5 Cross-Chain | Cross-Chain | Kanak | `backend/app/engines/crosschain/` |
| Stage 6 Risk Scoring | Risk Ensemble | Sristhi | `backend/app/engines/risk/` |
| Stage 7 Report | Dossier PDF | Kanak | `backend/app/reports/` |
| Stage 8 Delivery | Webhook & Audit | Himanshi | `backend/app/integrations/webhook.py`, `app/audit/` |
| TLS 1.3 Edge | Security | Kanak | `infra/caddy/Caddyfile` |
| Monitoring & Alerts | Metrics & Dashboard | Sristhi | `infra/prometheus/`, `infra/grafana/` |
