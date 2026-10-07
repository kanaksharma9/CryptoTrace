from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pydantic import Field
from typing import Literal
from .common import CT, Chain, Address, TxHash

class CrossChainLink(CT):
    case_id: UUID
    bridge: str # "polygon-pos", "synthetic-bridge"
    src_chain: Chain
    dst_chain: Chain
    src_tx: TxHash
    dst_tx: TxHash
    src_address: Address # who deposited
    dst_address: Address # who received
    src_amount: Decimal
    dst_amount: Decimal
    asset: str
    time_delta_s: int
    amount_ratio: float # dst/src
    match_score: float = Field(ge=0, le=1)
    method: str = "predicate_v1"
