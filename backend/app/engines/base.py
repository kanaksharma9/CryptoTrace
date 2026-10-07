from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from app.contracts import (
    Address,
    Attribution,
    Chain,
    CrossChainLink,
    EntityCluster,
    RiskScore,
    TraceGraph,
    TraceRequest,
    TxEdge,
)


class ChainDataProvider(Protocol):
    name: str

    async def head_block(self, chain: Chain) -> int: ...
    async def get_outgoing(
        self,
        chain: Chain,
        address: Address,
        *,
        after: datetime,
        before: datetime | None = None,
        max_items: int = 500,
    ) -> list[TxEdge]: ...
    async def get_incoming(
        self,
        chain: Chain,
        address: Address,
        *,
        after: datetime | None = None,
        before: datetime | None = None,
        max_items: int = 500,
    ) -> list[TxEdge]: ...
    async def is_contract(self, chain: Chain, address: Address) -> bool: ...
    async def balance(self, chain: Chain, address: Address, token: str | None = None) -> float: ...
    async def block_hash(self, chain: Chain, number: int) -> str: ...


class TracingEngine(Protocol):
    async def trace(self, req: TraceRequest) -> TraceGraph: ...


class ClusteringEngine(Protocol):
    async def cluster(self, graph: TraceGraph) -> list[EntityCluster]: ...


class AttributionEngine(Protocol):
    def attribute(self, graph: TraceGraph, clusters: Sequence[EntityCluster]) -> list[Attribution]: ...


class CrossChainEngine(Protocol):
    def match(self, graph: TraceGraph) -> list[CrossChainLink]: ...


class RiskEngine(Protocol):
    def score(
        self, graph: TraceGraph, addresses: Sequence[Address], clusters: Sequence[EntityCluster]
    ) -> list[RiskScore]: ...
