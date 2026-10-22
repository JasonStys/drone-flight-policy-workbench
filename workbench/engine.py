"""Jason Stys: checksum-verified fixed Rego execution and fail-closed result validation. Lines: docs/SOURCE_MAP.md."""

import json
import subprocess
import threading

from tools.fetch_opa import ROOT, binary
from workbench.models import Operation, Policy

GATE = threading.BoundedSemaphore(2)
STATUSES = {"satisfied", "blocked", "requires_review"}
REASONS = {
    "policy_context_or_window",
    "unknown_applicability",
    "not_applicable",
    "expired_evidence",
    "missing_evidence",
    "conflicting_evidence",
    "unknown_value",
    "future_evidence",
    "unattested_evidence",
    "stale_evidence",
    "configured_check_met",
    "configured_check_failed",
}
NOTICE = "Configured evidence only — not legal advice, airworthiness, flight authorization or a safe-to-fly verdict."


class EngineUnavailable(RuntimeError):
    """Unavailable/malformed policy decisions must never become satisfied evidence."""


def validate_result(value, policy):
    """Verify complete unique rule coverage and independently recompute overall hold precedence."""
    if (
        not isinstance(value, dict)
        or set(value) != {"status", "checks"}
        or not isinstance(value["checks"], list)
    ):
        raise ValueError("Malformed policy result")
    expected = {r.id for r in policy.rules}
    seen = set()
    for row in value["checks"]:
        if (
            not isinstance(row, dict)
            or set(row) != {"id", "status", "reason"}
            or row["id"] not in expected
            or row["id"] in seen
            or row["status"] not in STATUSES
            or row["reason"] not in REASONS
        ):
            raise ValueError("Incomplete or invalid rule evidence")
        seen.add(row["id"])
    statuses = {row["status"] for row in value["checks"]}
    status = (
        "blocked"
        if "blocked" in statuses
        else "requires_review"
        if "requires_review" in statuses
        else "satisfied"
    )
    if seen != expected or value["status"] != status:
        raise ValueError("Missing rules or inconsistent overall status")
    value["checks"].sort(key=lambda row: row["id"])
    return value


def evaluate(policy: Policy, operation: Operation):
    """Execute trusted pinned policy, data-only stdin, no shell, bounded process concurrency/runtime."""
    if not GATE.acquire(blocking=False):
        raise EngineUnavailable("Policy engine busy")
    try:
        command = [
            str(binary()),
            "eval",
            "--format=json",
            "--strict-builtin-errors",
            "--stdin-input",
            "--data",
            str(ROOT / "policies/flight.rego"),
            "data.flight.result",
        ]
        completed = subprocess.run(  # noqa: S603 - fixed checksum-verified vendor binary/query, no shell
            command,
            input=json.dumps(
                {"policy": policy.model_dump(), "operation": operation.model_dump()},
                allow_nan=False,
            ),
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        if completed.returncode or len(completed.stdout) > 128_000:
            raise ValueError("Policy engine failed")
        parsed = json.loads(completed.stdout)
        value = parsed["result"][0]["expressions"][0]["value"]
        result = validate_result(value, policy)
        result["notice"] = NOTICE
        result["flight_authorization"] = False
        return result
    except (
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        subprocess.TimeoutExpired,
    ) as error:
        raise EngineUnavailable(
            "OPA unavailable or returned invalid evidence; no assessment saved"
        ) from error
    finally:
        GATE.release()
