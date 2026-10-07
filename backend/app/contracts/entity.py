from enum import StrEnum

from pydantic import Field

from .common import CT, Address, Chain


class ClusterType(StrEnum):
    DEPOSIT_SWEEP = "deposit_sweep"  # many deposit addrs sweeping to one hub
    COSPEND = "cospend"  # stretch: UTXO co-input (Bitcoin)


class EntityCluster(CT):
    entity_id: str  # "ent_" + first 12 hex of sha256(sorted addresses + chain)
    chain: Chain
    cluster_type: ClusterType
    addresses: list[Address]
    hub_address: Address | None = None  # e.g. the hot wallet receiving the sweeps
    evidence: list[str] = []  # human-readable lines, e.g. "4 senders -> f1; 99% swept to hub in 300 s"
    score: float = Field(1.0, ge=0, le=1)
