import pathlib
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import UUID

from app.contracts import Chain, EdgeType, TxEdge

HERE = pathlib.Path(__file__).parent
T0 = datetime(2026, 9, 20, 10, 0, tzinfo=UTC)
CASE_ID = UUID("00000000-0000-0000-0000-000000000001")


def A(b: str) -> str:
    return "0x" + b * 20  # 0xa1a1...a1


a1, b1, b2, b3, c1 = A("a1"), A("b1"), A("b2"), A("b3"), A("c1")
f1, f0, d1, d2, e1 = A("f1"), A("f0"), A("d1"), A("d2"), A("e1")
f0p, x1, m1, f3 = A("f2"), A("dd"), A("ee"), A("f3")
senders = [A("91"), A("92"), A("93"), A("94")]
senders3 = [A("95"), A("96"), A("97")]

_n = 0


def tx(
    chain,
    src,
    dst,
    amt,
    minutes,
    sym="ETH",
    tok=None,
    etype=EdgeType.TRANSFER,
    h=None,
    li=0,
):
    global _n
    _n += 1
    h = h or "0x" + f"{_n:064x}"
    return TxEdge(
        tx_hash=h,
        log_index=li,
        chain=chain,
        src=src,
        dst=dst,
        token_symbol=sym,
        token_address=tok,
        amount=Decimal(str(amt)),
        timestamp=T0 + timedelta(minutes=minutes),
        block_number=20_000_000 + _n * 3 + minutes,
        block_hash="0x" + f"{_n:064x}",
        edge_type=etype,
    )


USDT = "0x" + "c0" * 20  # SYNTHETIC token address
swap_h = "0x" + "5" * 64
edges = [
    tx(Chain.ETH, a1, b1, 12.0, 0),
    tx(Chain.ETH, b1, b2, 5.9, 20),
    tx(Chain.ETH, b1, b3, 5.9, 22),
    tx(Chain.ETH, b2, c1, 5.9, 60, etype=EdgeType.SWAP, h=swap_h, li=0),
    tx(Chain.ETH, c1, b2, 17000, 60, "USDT", USDT, EdgeType.SWAP, h=swap_h, li=1),
    tx(Chain.ETH, b2, f1, 17000, 90, "USDT", USDT),
    *[
        tx(Chain.ETH, s, f1, amt, m, "USDT", USDT)
        for s, amt, m in zip(senders, [1000, 2500, 3100, 4000], [30, 50, 70, 85], strict=True)
    ],
    tx(Chain.ETH, f1, f0, 27600, 95, "USDT", USDT),
    tx(Chain.ETH, b2, x1, 0.01, 70),
    tx(Chain.ETH, b3, d1, 5.9, 30, etype=EdgeType.BRIDGE_IN),
    tx(Chain.POLYGON, d2, e1, 5.85, 55, "WETH", "0x" + "c5" * 20, EdgeType.BRIDGE_OUT),
    tx(Chain.POLYGON, e1, f0p, 5.85, 80, "WETH", "0x" + "c5" * 20),
    tx(Chain.ETH, b3, m1, 0.1, 40, etype=EdgeType.MIXER),
    *[
        tx(Chain.ETH, s, f3, amt, m, "USDT", USDT)
        for s, amt, m in zip(senders3, [1200, 800, 500], [40, 45, 50], strict=True)
    ],
    tx(Chain.ETH, f3, f0, 2500, 100, "USDT", USDT),  # second sweep into hub f0
]
