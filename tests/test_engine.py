"""Jason Stys: real OPA decisions vs independent Python oracle and strict contracts. Lines: docs/SOURCE_MAP.md."""

import copy
import json
import random
import subprocess

import pytest
from pydantic import ValidationError

from workbench import engine
from workbench.examples import example_operation, example_policy, examples
from workbench.models import Operation, Policy


def oracle(policy, operation):
    """Independent imperative rule semantics, without importing Rego or production decision code."""
    results = []

    def quality(key, age):
        """Compare every supplied assertion rather than selecting a convenient newest one."""
        records = [e for e in operation.evidence if e.fact == key]
        if not records:
            return "missing_evidence"
        if any(e.value != records[0].value for e in records):
            return "conflicting_evidence"
        if any(e.value is None for e in records):
            return "unknown_value"
        if any(e.observed_s > operation.as_of_s for e in records):
            return "future_evidence"
        if any(not e.attested for e in records):
            return "unattested_evidence"
        if any(e.expires_s <= operation.as_of_s for e in records):
            return "expired_evidence"
        if any(operation.as_of_s - e.observed_s > age for e in records):
            return "stale_evidence"
        return "usable"

    def value(key):
        """Quality has already established all supplied values agree."""
        return next(e.value for e in operation.evidence if e.fact == key)

    for rule in policy.rules:
        status, reason = "requires_review", "policy_context_or_window"
        if (
            operation.jurisdiction == policy.jurisdiction
            and operation.framework == policy.framework
            and policy.valid_from_s <= operation.as_of_s < policy.valid_until_s
        ):
            if rule.when_fact and quality(rule.when_fact, rule.max_age_s) != "usable":
                reason = "unknown_applicability"
            elif rule.when_fact and value(rule.when_fact) != rule.when_value:
                status, reason = "satisfied", "not_applicable"
            else:
                reason = quality(rule.fact, rule.max_age_s)
                if reason == "expired_evidence":
                    status = "blocked"
                elif reason == "usable":
                    actual = value(rule.fact)
                    met = (
                        actual == rule.expected
                        if rule.comparator == "equals"
                        else actual <= rule.expected
                        if rule.comparator == "max"
                        else actual >= rule.expected
                    )
                    status, reason = (
                        ("satisfied", "configured_check_met")
                        if met
                        else ("blocked", "configured_check_failed")
                    )
        results.append({"id": rule.id, "status": status, "reason": reason})
    statuses = [r["status"] for r in results]
    overall = (
        "blocked"
        if "blocked" in statuses
        else "requires_review"
        if "requires_review" in statuses
        else "satisfied"
    )
    return {"status": overall, "checks": sorted(results, key=lambda r: r["id"])}


def change(fact, **changes):
    """Edit one synthetic fixture without changing production schema defaults."""
    data = example_operation().model_dump()
    for e in data["evidence"]:
        if e["fact"] == fact:
            e.update(changes)
    return Operation.model_validate(data)


@pytest.mark.parametrize(
    "kind,status",
    [
        ("inspection", "satisfied"),
        ("missing-approval", "requires_review"),
        ("privacy-hold", "blocked"),
        ("expired-record", "blocked"),
    ],
)
def test_examples_real_opa(kind, status):
    """Each documented example runs through the checksum-verified actual OPA executable."""
    policy = example_policy()
    operation = Operation.model_validate(examples()[kind])
    result = engine.evaluate(policy, operation)
    assert {k: result[k] for k in ("status", "checks")} == oracle(policy, operation)
    assert result["status"] == status and result["flight_authorization"] is False


@pytest.mark.parametrize(
    "changes,reason,status",
    [
        ({"value": False}, "configured_check_failed", "blocked"),
        ({"value": None}, "unknown_value", "requires_review"),
        ({"attested": False}, "unattested_evidence", "requires_review"),
        ({"observed_s": 1001}, "future_evidence", "requires_review"),
        ({"expires_s": 1000}, "expired_evidence", "blocked"),
        ({"observed_s": 699}, "stale_evidence", "requires_review"),
        ({"observed_s": 700}, "configured_check_met", "satisfied"),
    ],
)
def test_evidence_precedence(changes, reason, status):
    """Exact expiry/freshness boundaries and missing/untrusted values fail as documented."""
    result = engine.evaluate(example_policy(), change("credential_current", **changes))
    row = next(r for r in result["checks"] if r["id"] == "credential")
    assert row["reason"] == reason and row["status"] == status


def test_conditional_unknown_and_false():
    """Unknown applicability is a review hold; explicit current false is not-applicable only."""
    for value, expected in [(None, "unknown_applicability"), (False, "not_applicable")]:
        result = engine.evaluate(example_policy(), change("controlled_airspace", value=value))
        assert next(r for r in result["checks"] if r["id"] == "airspace")["reason"] == expected


@pytest.mark.parametrize(
    "field,value",
    [
        ("jurisdiction", "OTHER"),
        ("jurisdiction", "UNKNOWN"),
        ("framework", "OTHER"),
        ("as_of_s", 899),
        ("as_of_s", 2000),
    ],
)
def test_context_and_policy_expiry(field, value):
    """No implicit US/Part107 applicability or stale policy assurance."""
    data = example_operation().model_dump()
    data[field] = value
    result = engine.evaluate(example_policy(), Operation.model_validate(data))
    assert result["status"] == "requires_review"
    assert {row["reason"] for row in result["checks"]} == {"policy_context_or_window"}


def test_conflicting_claims_and_permutation():
    """Contradictory current/old reports remain visible; input ordering cannot hide them."""
    data = example_operation().model_dump()
    extra = copy.deepcopy(data["evidence"][0])
    extra.update(id="contradiction", value=False)
    data["evidence"].append(extra)
    a = engine.evaluate(example_policy(), Operation.model_validate(data))
    data["evidence"].reverse()
    b = engine.evaluate(example_policy(), Operation.model_validate(data))
    assert a == b and a["status"] == "requires_review"


def test_seeded_oracle_and_numeric_operators():
    """100 varied real OPA runs plus independent per-rule/aggregate checks, deterministic seed."""
    rng = random.Random(20261022)  # noqa: S311 - deterministic mathematical fixtures, not credentials
    for _ in range(100):
        policy = example_policy().model_dump()
        operation = example_operation().model_dump()
        rule = rng.choice(policy["rules"])
        if rule["fact"] in ("altitude_agl_m", "wind_mps", "retention_days"):
            rule["comparator"] = rng.choice(["equals", "max", "min"])
        record = rng.choice(operation["evidence"])
        if type(record["value"]) is bool:
            record["value"] = rng.choice([True, False, None])
        else:
            record["value"] = rng.choice([None, 0.0, 100.0, 7.0, 8.0])
        record["attested"] = rng.choice([True, False])
        record["observed_s"] = rng.choice([650, 990, 1001])
        record["expires_s"] = 1100
        p = Policy.model_validate(policy)
        o = Operation.model_validate(operation)
        result = engine.evaluate(p, o)
        assert {k: result[k] for k in ("status", "checks")} == oracle(p, o)


@pytest.mark.parametrize(
    "changes",
    [
        {"value": "true"},
        {"value": 1.0},
        {"observed_s": -1},
        {"expires_s": 980},
        {"extra": "ignored"},
    ],
)
def test_invalid_evidence(changes):
    """No type coercion, reversed windows, extra fields or negative clocks."""
    with pytest.raises(ValidationError):
        change("credential_current", **changes)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda p: p["rules"].append(p["rules"][0]),
        lambda p: p.update(rules=[]),
        lambda p: p.update(valid_until_s=900),
        lambda p: p["rules"][0].update(comparator="min"),
        lambda p: p["rules"][0].update(expected=None),
        lambda p: p["rules"][0].update(when_fact="wind_mps"),
        lambda p: p["rules"][0].update(when_fact="credential_current"),
        lambda p: p["rules"][0].update(source_url="javascript:alert(1)"),
        lambda p: p["rules"][0].update(source_url="http://example.com/"),
        lambda p: p["rules"][0].update(expected="true"),
        lambda p: p["rules"][9].update(expected=True),
    ],
)
def test_invalid_policy(mutation):
    """Deny untyped executable-looking data and inconsistent rule shapes."""
    data = example_policy().model_dump()
    mutation(data)
    with pytest.raises(ValidationError):
        Policy.model_validate(data)


def test_policy_contradictions():
    """Detect boolean conflicts and incompatible numeric bounds before publication."""
    for index, changes in [
        (0, {"expected": False}),
        (9, {"comparator": "min", "expected": 101.0}),
        (9, {"comparator": "equals", "expected": 101.0}),
    ]:
        data = example_policy().model_dump()
        duplicate = copy.deepcopy(data["rules"][index])
        duplicate.update(id="conflict", **changes)
        data["rules"].append(duplicate)
        with pytest.raises(ValidationError):
            Policy.model_validate(data)
    data = example_policy().model_dump()
    a = data["rules"][5]
    b = copy.deepcopy(a)
    b.update(id="opposite-condition", when_value=False, expected=False)
    data["rules"].append(b)
    assert Policy.model_validate(data)


@pytest.mark.parametrize("value", [-1.0, float("nan"), float("inf"), "80", True])
def test_invalid_numeric(value):
    """SI quantities cannot contain booleans, strings or nonfinite values."""
    with pytest.raises(ValidationError):
        change("altitude_agl_m", value=value)


def test_duplicate_and_bounds():
    """Cap rule/evidence cardinality and reject duplicate provenance IDs."""
    data = example_operation().model_dump()
    data["evidence"] *= 2
    with pytest.raises(ValidationError):
        Operation.model_validate(data)
    data["evidence"] *= 10
    with pytest.raises(ValidationError):
        Operation.model_validate(data)
    data = example_policy().model_dump()
    data["rules"] *= 4
    with pytest.raises(ValidationError):
        Policy.model_validate(data)


@pytest.mark.parametrize(
    "output",
    [
        "{}",
        "not-json",
        '{"result":[]}',
        json.dumps(
            {"result": [{"expressions": [{"value": {"status": "satisfied", "checks": []}}]}]}
        ),
    ],
)
def test_malformed_result(monkeypatch, output):
    """Fail closed on undefined, partial or invalid engine output, not a fabricated success."""
    monkeypatch.setattr(
        subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess([], 0, output, "")
    )
    with pytest.raises(engine.EngineUnavailable):
        engine.evaluate(example_policy(), example_operation())


def test_output_inventory_and_aggregate():
    """Independent result gate rejects omitted/duplicate rules, unknown states and reassuring aggregate."""
    policy = example_policy()
    valid = oracle(policy, example_operation())
    for mutation in [
        lambda r: r["checks"].pop(),
        lambda r: r["checks"].append(r["checks"][0]),
        lambda r: r["checks"][0].update(status="approved"),
        lambda r: r.update(status="blocked"),
        lambda r: r["checks"][0].update(reason="unknown_reason"),
    ]:
        data = copy.deepcopy(valid)
        mutation(data)
        with pytest.raises(ValueError):
            engine.validate_result(data, policy)


@pytest.mark.parametrize("error", [OSError(), ValueError(), subprocess.TimeoutExpired("opa", 5)])
def test_unavailable(monkeypatch, error):
    """Checksum/missing binary/timeout paths are explicit failures with semaphore recovery."""

    def fail():
        """Simulate only the boundary failure; other tests execute actual OPA."""
        raise error

    monkeypatch.setattr(engine, "binary", fail)
    with pytest.raises(engine.EngineUnavailable):
        engine.evaluate(example_policy(), example_operation())


def test_busy_nonzero_oversize(monkeypatch):
    """Overload and bad process outcomes cannot be interpreted as satisfied checks."""
    engine.GATE.acquire()
    engine.GATE.acquire()
    try:
        with pytest.raises(engine.EngineUnavailable):
            engine.evaluate(example_policy(), example_operation())
    finally:
        engine.GATE.release()
        engine.GATE.release()
    for code, output in [(2, ""), (0, "x" * 128001)]:
        monkeypatch.setattr(
            subprocess,
            "run",
            lambda *a, code=code, output=output, **kw: subprocess.CompletedProcess(
                [], code, output, ""
            ),
        )
        with pytest.raises(engine.EngineUnavailable):
            engine.evaluate(example_policy(), example_operation())
