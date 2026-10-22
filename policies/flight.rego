# Jason Stys: deterministic preflight evidence policy; functions/variables: docs/SOURCE_MAP.md.
# All times are an explicit synthetic exercise clock. No network builtins or external authority.
package flight

import rego.v1

# Select claims without dropping contradictory or expired information.
records(key) := [e | some e in input.operation.evidence; e.fact == key]

# Fail conservatively in a documented precedence order; all supplied claims must agree and be current.
quality(key, age) := "missing_evidence" if {
	count(records(key)) == 0
} else := "conflicting_evidence" if {
	count({e.value | some e in records(key)}) > 1
} else := "unknown_value" if {
	some e in records(key)
	e.value == null
} else := "future_evidence" if {
	some e in records(key)
	e.observed_s > input.operation.as_of_s
} else := "unattested_evidence" if {
	some e in records(key)
	not e.attested
} else := "expired_evidence" if {
	some e in records(key)
	e.expires_s <= input.operation.as_of_s
} else := "stale_evidence" if {
	some e in records(key)
	input.operation.as_of_s - e.observed_s > age
} else := "usable"

# Unknown jurisdiction/framework and expired source-review windows cannot be presumed applicable.
context_ok if {
	input.operation.jurisdiction == input.policy.jurisdiction
	input.operation.framework == input.policy.framework
	input.operation.as_of_s >= input.policy.valid_from_s
	input.operation.as_of_s < input.policy.valid_until_s
}

# Conditional applicability also needs current, consistent, attested evidence.
applicability(rule) := "active" if {
	rule.when_fact == null
} else := "unknown" if {
	quality(rule.when_fact, rule.max_age_s) != "usable"
} else := "active" if {
	records(rule.when_fact)[0].value == rule.when_value
} else := "not_applicable"

# Comparisons operate only on schema-validated like-typed quantities.
matches(rule, value) if {
	rule.comparator == "equals"
	value == rule.expected
}

matches(rule, value) if {
	rule.comparator == "max"
	value <= rule.expected
}

matches(rule, value) if {
	rule.comparator == "min"
	value >= rule.expected
}

# A green row means configured evidence satisfied, never permission to conduct a flight.
check(rule) := {"status": "requires_review", "reason": "policy_context_or_window"} if {
	not context_ok
} else := {"status": "requires_review", "reason": "unknown_applicability"} if {
	applicability(rule) == "unknown"
} else := {"status": "satisfied", "reason": "not_applicable"} if {
	applicability(rule) == "not_applicable"
} else := {"status": "blocked", "reason": "expired_evidence"} if {
	quality(rule.fact, rule.max_age_s) == "expired_evidence"
} else := {"status": "requires_review", "reason": quality(rule.fact, rule.max_age_s)} if {
	quality(rule.fact, rule.max_age_s) != "usable"
} else := {"status": "satisfied", "reason": "configured_check_met"} if {
	matches(rule, records(rule.fact)[0].value)
} else := {"status": "blocked", "reason": "configured_check_failed"}

# Preserve one result per rule and deterministic strongest-hold aggregation.
checks := [object.union({"id": rule.id}, check(rule)) | some rule in input.policy.rules]

overall := "blocked" if {
	some row in checks
	row.status == "blocked"
} else := "requires_review" if {
	some row in checks
	row.status == "requires_review"
} else := "satisfied"

result := {"status": overall, "checks": checks}
