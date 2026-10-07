from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pydantic import Field
from typing import Literal
from .common import CT, Chain, Address, TxHash

class EvidenceTier(str, Enum):
    CONFIRMED = "confirmed" # terminal IS a tier-A labelled VASP address
    PROBABLE = "probable" # confidence >= 0.70 via behaviour linked to a labelled hub
    POSSIBLE = "possible" # 0.40 <= confidence < 0.70
    UNKNOWN = "unknown" # < 0.40, no VASP named

class HeuristicHit(CT):
    code: Literal["H1", "H2", "H3", "H4", "H5", "H6"]
    name: str
    fired: bool
    weight: float # configured weight
    contribution: float # weight if fired else 0 (or partial)
    detail: str # one-line explanation shown to investigators

class Attribution(CT):
    case_id: UUID
    chain: Chain
    terminal_address: Address
    entity_id: str | None = None
    vasp_id: str | None = None
    vasp_name: str | None = None
    hop_distance: int # hops from seed (number 1)
    proximity_rank: int | None = None # 1 = nearest VASP candidate (number 1: how close)
    confidence: float = Field(ge=0, le=1) # independent of proximity. NEVER blended.
    evidence_tier: EvidenceTier
    heuristics: list[HeuristicHit]
    label_source: str | None = None # e.g. "manual-curated", "synthetic"
    needs_review: bool = False
    path_tx_hashes: list[TxHash] = [] # one best path seed -> terminal
