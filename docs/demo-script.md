# CryptoTrace 3-4 Minute Final Demo Script

This script walks through the live demonstration of CryptoTrace for judges and hackathon evaluators.

---

## Step 1: SAHYOG Mock Portal Ingestion (0:00 - 0:30)
1. Open the SAHYOG mock portal (`http://localhost:8100`).
2. Submit a signed complaint for suspect wallet `0xb1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1` (HMAC-SHA256 signed POST).
3. Demonstrate that the complaint immediately creates a case and triggers the Celery pipeline.

## Step 2: Real-time 8-Stage Progress Bar (0:30 - 1:00)
1. Navigate to the CryptoTrace Investigator Dashboard (`http://localhost:3000/cases`).
2. Show live progress updates via Server-Sent Events (SSE) as the pipeline transitions through the 8 stages:
   `INGEST` -> `TRACE` -> `CLUSTER` -> `ATTRIBUTE` -> `CROSSCHAIN` -> `RISK` -> `REPORT` -> `DELIVER`.

## Step 3: Interactive Graph Visualization (1:00 - 1:45)
1. Open the **Graph** tab for the active case.
2. Demonstrate the temporal order slider and swap node collapsing.
3. Highlight the cross-chain hop from **Ethereum** (`0xd1...`) to **Polygon** (`0xd2...`), and highlight the mixer touch node (`0xee...`).

## Step 4: Two-Number Attribution Panel (1:45 - 2:15)
1. Switch to the **Attribution** tab.
2. Point out deposit address `0xf1...`:
   - **Proximity rank**: `1` (nearest VASP candidate).
   - **Confidence**: `0.92` / **Evidence Tier**: `PROBABLE`.
3. Open the heuristic details table showing hits for rules `H1` - `H6`.
4. Demonstrate low-confidence address `0xdd...` appearing in the Review Queue for investigator decision.

## Step 5: Risk Scoring & SHAP Waterfall (2:15 - 2:45)
1. Click on the **Risk** tab.
2. Display the ensemble risk score (XGBoost + RevTrack + Isolation Forest).
3. Show the SHAP waterfall chart explaining feature contributions to the risk score.

## Step 6: Evidence & Merkle Audit Trail Verification (2:45 - 3:15)
1. Open the **Audit & Evidence** section.
2. Show the SHA-256 hashes for all 8 stage artifacts.
3. Click **Verify Audit Chain** to prove the Merkle tree root matches the tamper-evident ledger.
4. Download the generated **PDF Dossier** and preview the Exchange Freeze Request template.

## Step 7: Live Monitoring & Alerting (3:15 - 3:30)
1. Trigger a synthetic transaction outflow.
2. Show real-time alert pop-up on the dashboard.
3. Briefly show Prometheus `/metrics` and Grafana dashboard (`http://localhost:3001`).

## Step 8: Wrap-up & Benchmark Metrics (3:30 - 3:45)
1. Present measured benchmark metrics: 3-hop trace completed in < 30 seconds on fixture data.
2. Emphasize that 100% of infrastructure runs on free and open-source tools with zero reliance on paid API services.
