from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pydantic import Field
from typing import Literal
from .common import CT, Chain, Address, TxHash

class PipelineEvent(CT):
    case_id: UUID
    stage: Literal["ingest","trace","cluster","attribute","crosschain","risk","report","deliver"]
    state: Literal["started","progress","done","failed"]
    pct: int = Field(0, ge=0, le=100)
    message: str = ""
    artifact_sha256: str | None = None
    ts: datetime

class Alert(CT):
    alert_id: UUID
    case_id: UUID
    chain: Chain
    address: Address
    kind: Literal["new_outflow","reached_vasp","bridge_used","mixer_used"]
    tx_hash: TxHash
    amount: Decimal | None = None
    message: str
    ts: datetime
