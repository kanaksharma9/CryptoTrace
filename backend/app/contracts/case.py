from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pydantic import Field
from typing import Literal
from .common import CT, Chain, Address, TxHash

class CaseSource(str, Enum):
    NCRP = "ncrp"; SAHYOG = "sahyog"; MANUAL = "manual"

class CaseStatus(str, Enum):
    RECEIVED="received"; TRACING="tracing"; CLUSTERING="clustering"; ATTRIBUTING="attributing"
    CROSSCHAIN="crosschain"; SCORING="scoring"; REPORTING="reporting"; DELIVERED="delivered"
    NEEDS_REVIEW="needs_review"; FAILED="failed"

class ComplaintIn(CT):
    complaint_ref: str # e.g. "NCRP-2026-000123"
    source: CaseSource
    victim_wallet: Address
    suspect_wallet: Address | None = None # if given, tracing seeds here; else at victim_wallet
    chain: Chain
    tx_hash: TxHash | None = None
    incident_time: datetime
    amount_lost_inr: Decimal | None = None
    narrative: str = ""
    callback_url: str | None = None # SAHYOG webhook target

class CaseSummary(CT):
    case_id: UUID
    complaint_ref: str
    chain: Chain
    seed_address: Address
    status: CaseStatus
    created_at: datetime
    top_vasp: str | None = None
    top_confidence: float | None = None
