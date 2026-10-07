# CryptoTrace ML Ensemble Model Card

## 1. Overview
The CryptoTrace risk engine computes address risk scores using a 3-model ensemble:
1. **XGBoost Classifier**: Supervised classification trained on tabular transaction features.
2. **Isolation Forest**: Unsupervised anomaly detection on transaction patterns.
3. **RevTrack Structural Slot**: Structural motif evaluation / graph motif scoring.

Explainability is provided via **SHAP (SHapley Additive exPlanations)** waterfall charts for top feature contributions.

---

## 2. Feature Vector (22 Features Total)
- **17 Tabular Features**:
  - Outflow volume (USD, native asset)
  - Inflow volume (USD, native asset)
  - Transaction count (in/out)
  - Mean & max transaction amounts
  - Time delta between first & last seen
  - Out-degree / in-degree ratio
  - Token multiplicity count
  - Gas spending statistics
  - Time distribution entropy
  - Peeling chain ratio
- **5 Graph Features**:
  - APPR score ($p_s$)
  - Hop distance from seed
  - Distance to nearest VASP hub
  - PageRank centrality
  - Mixer proximity flag

---

## 3. Model Scoring & Output Format
- **Category**: `LOW` | `MEDIUM` | `HIGH` | `CRITICAL`
- **Output Score**: Normalized float $0.0 \le \text{score} \le 1.0$
- **Ensemble Confidence**: Normalized float $0.0 \le \text{confidence} \le 1.0$
- **SHAP Contributions**: Top 8 features by absolute SHAP value $|\text{shap}|$.
