"""Jason Stys: bounded worst-envelope OPA launch/verification measurements. Lines: docs/SOURCE_MAP.md."""

import copy
import json
import platform
import statistics
import time

from workbench.engine import evaluate
from workbench.examples import example_operation, example_policy
from workbench.models import Operation, Policy


def main():
    """20 real evaluations at40 rules/128 claims; include runtime checksum, process and protocol costs."""
    policy = example_policy().model_dump()
    operation = example_operation().model_dump()
    original = policy["rules"][0]
    record = operation["evidence"][0]
    policy["rules"] = [{**copy.deepcopy(original), "id": f"rule-{n}"} for n in range(40)]
    operation["evidence"] = [{**copy.deepcopy(record), "id": f"claim-{n}"} for n in range(128)]
    policy = Policy.model_validate(policy)
    operation = Operation.model_validate(operation)
    samples = []
    for _ in range(20):
        start = time.perf_counter()
        result = evaluate(policy, operation)
        samples.append((time.perf_counter() - start) * 1000)
        assert result["status"] == "satisfied" and len(result["checks"]) == 40
    print(
        json.dumps(
            {
                "platform": platform.platform(),
                "iterations": 20,
                "rules": 40,
                "claims": 128,
                "median_ms": round(statistics.median(samples), 3),
                "max_ms": round(max(samples), 3),
                "includes": "SHA256 verification + OPA process/compile/evaluate + protocol checks",
            },
            indent=2,
        )
    )
    assert max(samples) < 5000, (
        "Full-envelope calculation must stay within the nominal process deadline; not a real-time guarantee"
    )


if __name__ == "__main__":
    main()
