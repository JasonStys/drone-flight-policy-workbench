"""Jason Stys: non-publishing policy impact review. Declarations/variables: docs/SOURCE_MAP.md."""

from workbench.engine import evaluate
from workbench.models import Operation, Policy
from workbench.store import digest


def policy_impact(active: Policy, draft: Policy, operation: Operation):
    """Evaluate identical evidence/time under both policies; preserve removed/new checks explicitly."""
    before, after = evaluate(active, operation), evaluate(draft, operation)
    old_rules = {rule.id: rule.model_dump() for rule in active.rules}
    new_rules = {rule.id: rule.model_dump() for rule in draft.rules}
    old = {row["id"]: row for row in before["checks"]}
    new = {row["id"]: row for row in after["checks"]}
    checks = []
    for identifier in sorted(old.keys() | new.keys()):
        checks.append(
            {
                "id": identifier,
                "before": old.get(identifier),
                "after": new.get(identifier),
                "configuration_changed": old_rules.get(identifier) != new_rules.get(identifier),
                "decision_changed": old.get(identifier) != new.get(identifier),
            }
        )
    inputs = {
        "active_policy": active.model_dump(),
        "draft_policy": draft.model_dump(),
        "operation": operation.model_dump(),
    }
    return {
        **inputs,
        "input_hash": digest(inputs),
        "before": before,
        "after": after,
        "checks": checks,
        "published": False,
        "flight_authorization": False,
        "notice": "UNPUBLISHED DRAFT PREVIEW. Same supplied evidence and synthetic time; no policy, evaluation, review or audit record is saved. Publishing later invalidates prior sign-off eligibility. Configured checks are not legal authorization or proof of safe flight.",
    }
