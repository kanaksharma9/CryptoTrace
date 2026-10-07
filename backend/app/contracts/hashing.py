import hashlib
import json

from pydantic import BaseModel


def canonical_json(obj) -> bytes:
    """Deterministic JSON: sorted keys, no spaces, Decimals as strings, datetimes as ISO-8601 Z."""

    def default(o):
        if isinstance(o, BaseModel):
            return o.model_dump(mode="json")
        raise TypeError(type(o))

    data = obj.model_dump(mode="json") if isinstance(obj, BaseModel) else obj
    return json.dumps(data, sort_keys=True, separators=(",", ":"), default=default).encode()


def sha256_hex(obj) -> str:
    return hashlib.sha256(canonical_json(obj)).hexdigest()
