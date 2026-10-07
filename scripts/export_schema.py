import json, pathlib, sys
sys.path.insert(0, "backend")
from pydantic import TypeAdapter
from app import contracts as c
names = ["TraceRequest","TraceGraph","EntityCluster","Attribution","CrossChainLink","RiskScore",
         "ComplaintIn","CaseSummary","PipelineEvent","Alert"]
out = {n: getattr(c, n).model_json_schema() for n in names}
out["_version"] = c.CONTRACT_VERSION
p = pathlib.Path("docs/contracts/schema.json")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("wrote", p)
