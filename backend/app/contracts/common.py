from __future__ import annotations
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator

CONTRACT_VERSION = "1.0.0"

class Chain(str, Enum):
    ETH = "eth"
    BSC = "bsc"
    POLYGON = "polygon"

CHAIN_IDS = {Chain.ETH: 1, Chain.BSC: 56, Chain.POLYGON: 137}
NATIVE_SYMBOL = {Chain.ETH: "ETH", Chain.BSC: "BNB", Chain.POLYGON: "POL"}

def _lower(v):
    return v.lower() if isinstance(v, str) else v

# ALWAYS lower-case 0x + 40 hex inside the system. Checksum (EIP-55) is validated only at ingestion.
Address = Annotated[str, BeforeValidator(_lower), Field(pattern=r"^0x[a-f0-9]{40}$")]
TxHash = Annotated[str, BeforeValidator(_lower), Field(pattern=r"^0x[a-f0-9]{64}$")]

class CT(BaseModel):
    """Base for every contract. extra=forbid so typos fail loudly."""
    model_config = ConfigDict(extra="forbid", use_enum_values=False)
