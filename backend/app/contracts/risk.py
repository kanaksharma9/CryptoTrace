from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pydantic import Field
from typing import Literal
from .common import CT, Chain, Address, TxHash

class RiskCategory(str, Enum):
    LOW = "low"; MEDIUM = "medium"; HIGH = "high"; CRITICAL = "critical"

class ShapContribution(CT):
    feature: str
    value: float # the feature value for this address
    shap: float # signed contribution to the XGBoost output (log-odds)

class ModelScores(CT):
    xgboost: float | None = None
    revtrack: float | None = None # may be the structural fallback; see revtrack_mode
    isoforest: float | None = None
    revtrack_mode: Literal["pretrained", "fallback", "off"] = "off"

class RiskScore(CT):
    case_id: UUID
    chain: Chain
    address: Address
    score: float = Field(ge=0, le=1)
    category: RiskCategory
    model_scores: ModelScores
    ensemble_confidence: float = Field(ge=0, le=1)
    shap_top: list[ShapContribution] # top 8 by |shap|
    features: dict[str, float] # the 17 tabular + 5 graph features, for the evidence file
    model_version: str # "xgb_v1|iso_v1|rev_v0"
    input_hash: str # sha256 of canonical features dict
    scored_at: datetime
