# Jason Stys: independent native Rego decision-table cases; variable/rule lines: docs/SOURCE_MAP.md.
package flight_test

import data.flight
import rego.v1

sample_rule := {"id": "r", "fact": "vlos_plan", "comparator": "equals", "expected": true, "max_age_s": 300, "when_fact": null, "when_value": true}
sample_evidence := {"id": "e", "fact": "vlos_plan", "value": true, "observed_s": 990, "expires_s": 1100, "attested": true}
sample_policy := {"jurisdiction": "US", "framework": "PART_107", "valid_from_s": 900, "valid_until_s": 2000, "rules": [sample_rule]}
sample_operation := {"jurisdiction": "US", "framework": "PART_107", "as_of_s": 1000, "evidence": [sample_evidence]}

# Exhaust quality precedence and both definitive comparison outcomes.
test_decision_table if {
	cases := [
		{"evidence": [], "status": "requires_review", "reason": "missing_evidence"},
		{"evidence": [sample_evidence, object.union(sample_evidence, {"value": false})], "status": "requires_review", "reason": "conflicting_evidence"},
		{"evidence": [object.union(sample_evidence, {"value": null})], "status": "requires_review", "reason": "unknown_value"},
		{"evidence": [object.union(sample_evidence, {"observed_s": 1001})], "status": "requires_review", "reason": "future_evidence"},
		{"evidence": [object.union(sample_evidence, {"attested": false})], "status": "requires_review", "reason": "unattested_evidence"},
		{"evidence": [object.union(sample_evidence, {"expires_s": 1000})], "status": "blocked", "reason": "expired_evidence"},
		{"evidence": [object.union(sample_evidence, {"observed_s": 699})], "status": "requires_review", "reason": "stale_evidence"},
		{"evidence": [object.union(sample_evidence, {"value": false})], "status": "blocked", "reason": "configured_check_failed"},
		{"evidence": [sample_evidence], "status": "satisfied", "reason": "configured_check_met"},
	]
	every tc in cases {
		operation := object.union(sample_operation, {"evidence": tc.evidence})
		result := flight.result with input as {"policy": sample_policy, "operation": operation}
		result.status == tc.status
		result.checks[0].reason == tc.reason
	}
}

# Applicability needs trusted condition evidence; false never becomes permission.
test_conditions if {
	rule := object.union(sample_rule, {"when_fact": "controlled_airspace"})
	policy := object.union(sample_policy, {"rules": [rule]})
	every tc in [{"value": null, "reason": "unknown_applicability"}, {"value": false, "reason": "not_applicable"}, {"value": true, "reason": "configured_check_met"}] {
		condition := object.union(sample_evidence, {"id": "condition", "fact": "controlled_airspace", "value": tc.value})
		operation := object.union(sample_operation, {"evidence": [sample_evidence, condition]})
		result := flight.result with input as {"policy": policy, "operation": operation}
		result.checks[0].reason == tc.reason
	}
}

# Both independent numeric comparisons and exact equality are exercised.
test_numeric_comparators if {
	evidence := object.union(sample_evidence, {"fact": "altitude_agl_m", "value": 100})
	every comparator in ["equals", "max", "min"] {
		rule := object.union(sample_rule, {"fact": "altitude_agl_m", "expected": 100, "comparator": comparator})
		policy := object.union(sample_policy, {"rules": [rule]})
		operation := object.union(sample_operation, {"evidence": [evidence]})
		result := flight.result with input as {"policy": policy, "operation": operation}
		result.status == "satisfied"
	}
}

# Expired policy and mismatched jurisdiction cannot produce a definite positive assessment.
test_context if {
	every changes in [{"jurisdiction": "UNKNOWN"}, {"framework": "OTHER"}, {"as_of_s": 2000}, {"as_of_s": 899}] {
		operation := object.union(sample_operation, changes)
		result := flight.result with input as {"policy": sample_policy, "operation": operation}
		result.status == "requires_review"
		result.checks[0].reason == "policy_context_or_window"
	}
}
