from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import Field

from .common import CT, Address, Chain, TxHash


class EdgeType(StrEnum):
    TRANSFER = "transfer"
    SWAP = "swap"  # token redirected inside one tx (in-token -> out-token)
    BRIDGE_IN = "bridge_in"  # deposit into a bridge contract
    BRIDGE_OUT = "bridge_out"
    MIXER = "mixer"


class TxEdge(CT):
    tx_hash: TxHash
    log_index: int = 0  # position inside tx so (tx_hash, log_index) is unique
    chain: Chain
    src: Address
    dst: Address
    token_symbol: str  # "ETH", "USDT", ...
    token_address: Address | None = None  # None = native coin
    amount: Decimal  # human units (not wei)
    amount_usd: Decimal | None = None
    timestamp: datetime  # tz-aware UTC
    block_number: int
    block_hash: str | None = None  # needed by ReorgGuard
    edge_type: EdgeType = EdgeType.TRANSFER


class TraceParams(CT):
    max_hops: int = Field(3, ge=1, le=6)
    alpha: float = Field(0.15, gt=0, lt=1)  # teleport / restart probability
    epsilon: float = Field(1e-4, gt=0)  # push threshold (smaller = deeper, slower)
    top_k: int = Field(200, ge=10)  # max nodes returned (by ttr_score)
    max_out_degree: int = Field(50, ge=5)  # per-node out-edge cap (biggest by weight kept)
    window_hours: int = Field(720, ge=1)  # only edges within seed_time + window
    confirmations: int = Field(12, ge=0)  # ignore blocks newer than head - confirmations


class TraceRequest(CT):
    case_id: UUID
    seed_address: Address
    chain: Chain
    seed_time: datetime
    params: TraceParams = TraceParams()


class TraceNode(CT):
    address: Address
    chain: Chain
    hop: int  # minimum hop distance from seed (bridge link counts as 1 hop)
    ttr_score: float  # APPR estimate p_s, 0..1
    is_contract: bool = False
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    tags: list[str] = []  # e.g. ["seed","dex_router","mixer","bridge","labelled_vasp"]
    entity_id: str | None = None  # filled by clustering


class TraceGraph(CT):
    case_id: UUID
    seed_address: Address
    chain: Chain
    nodes: list[TraceNode]
    edges: list[TxEdge]
    params: TraceParams
    truncated: bool = False  # True if top_k / degree caps removed something
    graph_hash: str  # sha256 of canonical JSON (see hashing.py)
    generated_at: datetime
