# Source declaration map

By Jason Stys. Headers link here for current exact physical lines.
Python/TypeScript ASTs index declarations, parameters and bindings. Rego lists rule/assignment/some/every lines; SQL lists non-comment schema lines. Lexical maps are navigation, not complete semantic symbol tables.

| File | Line | Declaration / variable |
| --- | ---: | --- |
| `policies/flight.rego` | 8 | `records(key) := [e / some e in input.operation.evidence; e.fact == key]` |
| `policies/flight.rego` | 11 | `quality(key, age) := "missing_evidence" if {` |
| `policies/flight.rego` | 13 | `} else := "conflicting_evidence" if {` |
| `policies/flight.rego` | 14 | `count({e.value / some e in records(key)}) > 1` |
| `policies/flight.rego` | 15 | `} else := "unknown_value" if {` |
| `policies/flight.rego` | 16 | `some e in records(key)` |
| `policies/flight.rego` | 18 | `} else := "future_evidence" if {` |
| `policies/flight.rego` | 19 | `some e in records(key)` |
| `policies/flight.rego` | 21 | `} else := "unattested_evidence" if {` |
| `policies/flight.rego` | 22 | `some e in records(key)` |
| `policies/flight.rego` | 24 | `} else := "expired_evidence" if {` |
| `policies/flight.rego` | 25 | `some e in records(key)` |
| `policies/flight.rego` | 27 | `} else := "stale_evidence" if {` |
| `policies/flight.rego` | 28 | `some e in records(key)` |
| `policies/flight.rego` | 30 | `} else := "usable"` |
| `policies/flight.rego` | 33 | `context_ok if {` |
| `policies/flight.rego` | 41 | `applicability(rule) := "active" if {` |
| `policies/flight.rego` | 43 | `} else := "unknown" if {` |
| `policies/flight.rego` | 45 | `} else := "active" if {` |
| `policies/flight.rego` | 47 | `} else := "not_applicable"` |
| `policies/flight.rego` | 50 | `matches(rule, value) if {` |
| `policies/flight.rego` | 55 | `matches(rule, value) if {` |
| `policies/flight.rego` | 60 | `matches(rule, value) if {` |
| `policies/flight.rego` | 66 | `check(rule) := {"status": "requires_review", "reason": "policy_context_or_window"} if {` |
| `policies/flight.rego` | 68 | `} else := {"status": "requires_review", "reason": "unknown_applicability"} if {` |
| `policies/flight.rego` | 70 | `} else := {"status": "satisfied", "reason": "not_applicable"} if {` |
| `policies/flight.rego` | 72 | `} else := {"status": "blocked", "reason": "expired_evidence"} if {` |
| `policies/flight.rego` | 74 | `} else := {"status": "requires_review", "reason": quality(rule.fact, rule.max_age_s)} if {` |
| `policies/flight.rego` | 76 | `} else := {"status": "satisfied", "reason": "configured_check_met"} if {` |
| `policies/flight.rego` | 78 | `} else := {"status": "blocked", "reason": "configured_check_failed"}` |
| `policies/flight.rego` | 81 | `checks := [object.union({"id": rule.id}, check(rule)) / some rule in input.policy.rules]` |
| `policies/flight.rego` | 83 | `overall := "blocked" if {` |
| `policies/flight.rego` | 84 | `some row in checks` |
| `policies/flight.rego` | 86 | `} else := "requires_review" if {` |
| `policies/flight.rego` | 87 | `some row in checks` |
| `policies/flight.rego` | 89 | `} else := "satisfied"` |
| `policies/flight.rego` | 91 | `result := {"status": overall, "checks": checks}` |
| `policies/flight_test.rego` | 7 | `sample_rule := {"id": "r", "fact": "vlos_plan", "comparator": "equals", "expected": true, "max_age_s": 300, "when_fact": null, "when_value": true}` |
| `policies/flight_test.rego` | 8 | `sample_evidence := {"id": "e", "fact": "vlos_plan", "value": true, "observed_s": 990, "expires_s": 1100, "attested": true}` |
| `policies/flight_test.rego` | 9 | `sample_policy := {"jurisdiction": "US", "framework": "PART_107", "valid_from_s": 900, "valid_until_s": 2000, "rules": [sample_rule]}` |
| `policies/flight_test.rego` | 10 | `sample_operation := {"jurisdiction": "US", "framework": "PART_107", "as_of_s": 1000, "evidence": [sample_evidence]}` |
| `policies/flight_test.rego` | 13 | `test_decision_table if {` |
| `policies/flight_test.rego` | 14 | `cases := [` |
| `policies/flight_test.rego` | 25 | `every tc in cases {` |
| `policies/flight_test.rego` | 26 | `operation := object.union(sample_operation, {"evidence": tc.evidence})` |
| `policies/flight_test.rego` | 27 | `result := flight.result with input as {"policy": sample_policy, "operation": operation}` |
| `policies/flight_test.rego` | 34 | `test_conditions if {` |
| `policies/flight_test.rego` | 35 | `rule := object.union(sample_rule, {"when_fact": "controlled_airspace"})` |
| `policies/flight_test.rego` | 36 | `policy := object.union(sample_policy, {"rules": [rule]})` |
| `policies/flight_test.rego` | 37 | `every tc in [{"value": null, "reason": "unknown_applicability"}, {"value": false, "reason": "not_applicable"}, {"value": true, "reason": "configured_check_met"}] {` |
| `policies/flight_test.rego` | 38 | `condition := object.union(sample_evidence, {"id": "condition", "fact": "controlled_airspace", "value": tc.value})` |
| `policies/flight_test.rego` | 39 | `operation := object.union(sample_operation, {"evidence": [sample_evidence, condition]})` |
| `policies/flight_test.rego` | 40 | `result := flight.result with input as {"policy": policy, "operation": operation}` |
| `policies/flight_test.rego` | 46 | `test_numeric_comparators if {` |
| `policies/flight_test.rego` | 47 | `evidence := object.union(sample_evidence, {"fact": "altitude_agl_m", "value": 100})` |
| `policies/flight_test.rego` | 48 | `every comparator in ["equals", "max", "min"] {` |
| `policies/flight_test.rego` | 49 | `rule := object.union(sample_rule, {"fact": "altitude_agl_m", "expected": 100, "comparator": comparator})` |
| `policies/flight_test.rego` | 50 | `policy := object.union(sample_policy, {"rules": [rule]})` |
| `policies/flight_test.rego` | 51 | `operation := object.union(sample_operation, {"evidence": [evidence]})` |
| `policies/flight_test.rego` | 52 | `result := flight.result with input as {"policy": policy, "operation": operation}` |
| `policies/flight_test.rego` | 58 | `test_context if {` |
| `policies/flight_test.rego` | 59 | `every changes in [{"jurisdiction": "UNKNOWN"}, {"framework": "OTHER"}, {"as_of_s": 2000}, {"as_of_s": 899}] {` |
| `policies/flight_test.rego` | 60 | `operation := object.union(sample_operation, changes)` |
| `policies/flight_test.rego` | 61 | `result := flight.result with input as {"policy": sample_policy, "operation": operation}` |
| `tests/test_api_store.py` | 16 | `PASSWORD` |
| `tests/test_api_store.py` | 17 | `ORIGIN` |
| `tests/test_api_store.py` | 21 | `application(tmp_path)` |
| `tests/test_api_store.py` | 23 | `app` |
| `tests/test_api_store.py` | 25 | `name` |
| `tests/test_api_store.py` | 25 | `role` |
| `tests/test_api_store.py` | 35 | `client(app, name)` |
| `tests/test_api_store.py` | 37 | `value` |
| `tests/test_api_store.py` | 38 | `response` |
| `tests/test_api_store.py` | 46 | `evaluate(value, operation)` |
| `tests/test_api_store.py` | 48 | `version` |
| `tests/test_api_store.py` | 55 | `test_end_to_end_independent_acknowledgement(application)` |
| `tests/test_api_store.py` | 57 | `operator` |
| `tests/test_api_store.py` | 58 | `reviewer` |
| `tests/test_api_store.py` | 59 | `response` |
| `tests/test_api_store.py` | 61 | `identifier` |
| `tests/test_api_store.py` | 62 | `report` |
| `tests/test_api_store.py` | 68 | `reviewed` |
| `tests/test_api_store.py` | 90 | `test_private_objects_and_roles(application)` |
| `tests/test_api_store.py` | 92 | `operator` |
| `tests/test_api_store.py` | 93 | `other` |
| `tests/test_api_store.py` | 94 | `admin` |
| `tests/test_api_store.py` | 95 | `identifier` |
| `tests/test_api_store.py` | 101 | `payload` |
| `tests/test_api_store.py` | 123 | `test_self_review_and_holds(application)` |
| `tests/test_api_store.py` | 125 | `reviewer` |
| `tests/test_api_store.py` | 126 | `operator` |
| `tests/test_api_store.py` | 127 | `own` |
| `tests/test_api_store.py` | 134 | `status` |
| `tests/test_api_store.py` | 135 | `operation` |
| `tests/test_api_store.py` | 137 | `identifier` |
| `tests/test_api_store.py` | 154 | `test_origin_csrf_size_and_headers(application)` |
| `tests/test_api_store.py` | 156 | `value` |
| `tests/test_api_store.py` | 175 | `invalid` |
| `tests/test_api_store.py` | 185 | `test_login_expiry_revocation_and_hashes(application)` |
| `tests/test_api_store.py` | 187 | `value` |
| `tests/test_api_store.py` | 188 | `token` |
| `tests/test_api_store.py` | 190 | `db` |
| `tests/test_api_store.py` | 199 | `value` |
| `tests/test_api_store.py` | 200 | `db` |
| `tests/test_api_store.py` | 208 | `test_login_failures_throttle_and_cookie(application)` |
| `tests/test_api_store.py` | 210 | `value` |
| `tests/test_api_store.py` | 211 | `name` |
| `tests/test_api_store.py` | 220 | `response` |
| `tests/test_api_store.py` | 229 | `db` |
| `tests/test_api_store.py` | 249 | `test_provisioning_rejects_invalid(application, name, password, role)` |
| `tests/test_api_store.py` | 255 | `test_session_limit_attempt_capacity_and_cleanup(application)` |
| `tests/test_api_store.py` | 257 | `store` |
| `tests/test_api_store.py` | 258 | `db` |
| `tests/test_api_store.py` | 259 | `n` |
| `tests/test_api_store.py` | 266 | `db` |
| `tests/test_api_store.py` | 271 | `db` |
| `tests/test_api_store.py` | 273 | `n` |
| `tests/test_api_store.py` | 275 | `value` |
| `tests/test_api_store.py` | 286 | `test_engine_and_stale_persistence(application, monkeypatch)` |
| `tests/test_api_store.py` | 288 | `value` |
| `tests/test_api_store.py` | 290 | `fail()` |
| `tests/test_api_store.py` | 297 | `concurrent(policy, operation)` |
| `tests/test_api_store.py` | 307 | `test_atomic_version_race_and_immutable_rows(application)` |
| `tests/test_api_store.py` | 309 | `store` |
| `tests/test_api_store.py` | 311 | `publish()` |
| `tests/test_api_store.py` | 318 | `pool` |
| `tests/test_api_store.py` | 322 | `user` |
| `tests/test_api_store.py` | 323 | `identifier` |
| `tests/test_api_store.py` | 325 | `statement` |
| `tests/test_api_store.py` | 333 | `db` |
| `tests/test_api_store.py` | 338 | `test_corruption_missing_install_and_slow_body(application, tmp_path, monkeypatch)` |
| `tests/test_api_store.py` | 340 | `empty` |
| `tests/test_api_store.py` | 343 | `db` |
| `tests/test_api_store.py` | 351 | `Timeout(class)` |
| `tests/test_api_store.py` | 354 | `__aenter__(self)` |
| `tests/test_api_store.py` | 357 | `__aexit__(self)` |
| `tests/test_api_store.py` | 369 | `test_evaluation_corruption(application)` |
| `tests/test_api_store.py` | 371 | `value` |
| `tests/test_api_store.py` | 372 | `identifier` |
| `tests/test_api_store.py` | 373 | `db` |
| `tests/test_api_store.py` | 379 | `test_origin_port_validation()` |
| `tests/test_auth_capacity.py` | 16 | `test_verification_capacity_and_unknown_dummy(tmp_path)` |
| `tests/test_auth_capacity.py` | 18 | `app` |
| `tests/test_auth_capacity.py` | 20 | `value` |
| `tests/test_auth_capacity.py` | 24 | `response` |
| `tests/test_auth_capacity.py` | 33 | `response` |
| `tests/test_auth_capacity.py` | 43 | `test_real_server_forwarded_addresses_do_not_bypass_throttle(tmp_path)` |
| `tests/test_auth_capacity.py` | 45 | `listener` |
| `tests/test_auth_capacity.py` | 47 | `port` |
| `tests/test_auth_capacity.py` | 48 | `origin` |
| `tests/test_auth_capacity.py` | 49 | `app` |
| `tests/test_auth_capacity.py` | 50 | `server` |
| `tests/test_auth_capacity.py` | 60 | `thread` |
| `tests/test_auth_capacity.py` | 63 | `deadline` |
| `tests/test_auth_capacity.py` | 67 | `value` |
| `tests/test_auth_capacity.py` | 68 | `n` |
| `tests/test_auth_capacity.py` | 69 | `response` |
| `tests/test_cli.py` | 11 | `test_cli_setup_accounts_and_serve(tmp_path, monkeypatch)` |
| `tests/test_cli.py` | 13 | `path` |
| `tests/test_cli.py` | 17 | `answers` |
| `tests/test_cli.py` | 23 | `db` |
| `tests/test_cli.py` | 25 | `answers` |
| `tests/test_cli.py` | 28 | `calls` |
| `tests/test_engine.py` | 16 | `oracle(policy, operation)` |
| `tests/test_engine.py` | 18 | `results` |
| `tests/test_engine.py` | 20 | `quality(key, age)` |
| `tests/test_engine.py` | 22 | `e` |
| `tests/test_engine.py` | 22 | `records` |
| `tests/test_engine.py` | 25 | `e` |
| `tests/test_engine.py` | 27 | `e` |
| `tests/test_engine.py` | 29 | `e` |
| `tests/test_engine.py` | 31 | `e` |
| `tests/test_engine.py` | 33 | `e` |
| `tests/test_engine.py` | 35 | `e` |
| `tests/test_engine.py` | 39 | `value(key)` |
| `tests/test_engine.py` | 41 | `e` |
| `tests/test_engine.py` | 43 | `rule` |
| `tests/test_engine.py` | 44 | `reason` |
| `tests/test_engine.py` | 44 | `status` |
| `tests/test_engine.py` | 51 | `reason` |
| `tests/test_engine.py` | 53 | `reason` |
| `tests/test_engine.py` | 53 | `status` |
| `tests/test_engine.py` | 55 | `reason` |
| `tests/test_engine.py` | 57 | `status` |
| `tests/test_engine.py` | 59 | `actual` |
| `tests/test_engine.py` | 60 | `met` |
| `tests/test_engine.py` | 67 | `reason` |
| `tests/test_engine.py` | 67 | `status` |
| `tests/test_engine.py` | 73 | `r` |
| `tests/test_engine.py` | 73 | `statuses` |
| `tests/test_engine.py` | 74 | `overall` |
| `tests/test_engine.py` | 84 | `change(fact)` |
| `tests/test_engine.py` | 86 | `data` |
| `tests/test_engine.py` | 87 | `e` |
| `tests/test_engine.py` | 102 | `test_examples_real_opa(kind, status)` |
| `tests/test_engine.py` | 104 | `policy` |
| `tests/test_engine.py` | 105 | `operation` |
| `tests/test_engine.py` | 106 | `result` |
| `tests/test_engine.py` | 107 | `k` |
| `tests/test_engine.py` | 123 | `test_evidence_precedence(changes, reason, status)` |
| `tests/test_engine.py` | 125 | `result` |
| `tests/test_engine.py` | 126 | `r` |
| `tests/test_engine.py` | 126 | `row` |
| `tests/test_engine.py` | 130 | `test_conditional_unknown_and_false()` |
| `tests/test_engine.py` | 132 | `expected` |
| `tests/test_engine.py` | 132 | `value` |
| `tests/test_engine.py` | 133 | `result` |
| `tests/test_engine.py` | 134 | `r` |
| `tests/test_engine.py` | 147 | `test_context_and_policy_expiry(field, value)` |
| `tests/test_engine.py` | 149 | `data` |
| `tests/test_engine.py` | 151 | `result` |
| `tests/test_engine.py` | 153 | `row` |
| `tests/test_engine.py` | 156 | `test_conflicting_claims_and_permutation()` |
| `tests/test_engine.py` | 158 | `data` |
| `tests/test_engine.py` | 159 | `extra` |
| `tests/test_engine.py` | 162 | `a` |
| `tests/test_engine.py` | 164 | `b` |
| `tests/test_engine.py` | 168 | `test_seeded_oracle_and_numeric_operators()` |
| `tests/test_engine.py` | 170 | `rng` |
| `tests/test_engine.py` | 171 | `_` |
| `tests/test_engine.py` | 172 | `policy` |
| `tests/test_engine.py` | 173 | `operation` |
| `tests/test_engine.py` | 174 | `rule` |
| `tests/test_engine.py` | 177 | `record` |
| `tests/test_engine.py` | 185 | `p` |
| `tests/test_engine.py` | 186 | `o` |
| `tests/test_engine.py` | 187 | `result` |
| `tests/test_engine.py` | 188 | `k` |
| `tests/test_engine.py` | 201 | `test_invalid_evidence(changes)` |
| `tests/test_engine.py` | 223 | `test_invalid_policy(mutation)` |
| `tests/test_engine.py` | 225 | `data` |
| `tests/test_engine.py` | 231 | `test_policy_contradictions()` |
| `tests/test_engine.py` | 233 | `changes` |
| `tests/test_engine.py` | 233 | `index` |
| `tests/test_engine.py` | 238 | `data` |
| `tests/test_engine.py` | 239 | `duplicate` |
| `tests/test_engine.py` | 244 | `data` |
| `tests/test_engine.py` | 245 | `a` |
| `tests/test_engine.py` | 246 | `b` |
| `tests/test_engine.py` | 253 | `test_invalid_numeric(value)` |
| `tests/test_engine.py` | 259 | `test_duplicate_and_bounds()` |
| `tests/test_engine.py` | 261 | `data` |
| `tests/test_engine.py` | 268 | `data` |
| `tests/test_engine.py` | 285 | `test_malformed_result(monkeypatch, output)` |
| `tests/test_engine.py` | 294 | `test_output_inventory_and_aggregate()` |
| `tests/test_engine.py` | 296 | `policy` |
| `tests/test_engine.py` | 297 | `valid` |
| `tests/test_engine.py` | 298 | `mutation` |
| `tests/test_engine.py` | 305 | `data` |
| `tests/test_engine.py` | 312 | `test_unavailable(monkeypatch, error)` |
| `tests/test_engine.py` | 315 | `fail()` |
| `tests/test_engine.py` | 324 | `test_busy_nonzero_oversize(monkeypatch)` |
| `tests/test_engine.py` | 334 | `code` |
| `tests/test_engine.py` | 334 | `output` |
| `tests/test_osv_policy.py` | 12 | `lock()` |
| `tests/test_osv_policy.py` | 24 | `report()` |
| `tests/test_osv_policy.py` | 32 | `name` |
| `tests/test_osv_policy.py` | 32 | `version` |
| `tests/test_osv_policy.py` | 39 | `test_complete_inventory()` |
| `tests/test_osv_policy.py` | 41 | `expected` |
| `tests/test_osv_policy.py` | 55 | `test_invalid_lock(change)` |
| `tests/test_osv_policy.py` | 57 | `data` |
| `tests/test_osv_policy.py` | 82 | `test_incomplete_or_finding_never_passes(change)` |
| `tests/test_osv_policy.py` | 84 | `data` |
| `tools/audit_osv.py` | 17 | `ROOT` |
| `tools/audit_osv.py` | 18 | `VERSION` |
| `tools/audit_osv.py` | 19 | `BINARIES` |
| `tools/audit_osv.py` | 47 | `expected_packages(lock)` |
| `tools/audit_osv.py` | 51 | `expected` |
| `tools/audit_osv.py` | 52 | `location` |
| `tools/audit_osv.py` | 52 | `package` |
| `tools/audit_osv.py` | 55 | `name` |
| `tools/audit_osv.py` | 56 | `version` |
| `tools/audit_osv.py` | 73 | `verify_report(report, expected)` |
| `tools/audit_osv.py` | 81 | `scanned` |
| `tools/audit_osv.py` | 82 | `result` |
| `tools/audit_osv.py` | 83 | `source` |
| `tools/audit_osv.py` | 91 | `item` |
| `tools/audit_osv.py` | 92 | `package` |
| `tools/audit_osv.py` | 99 | `findings` |
| `tools/audit_osv.py` | 108 | `main()` |
| `tools/audit_osv.py` | 110 | `checksum` |
| `tools/audit_osv.py` | 110 | `name` |
| `tools/audit_osv.py` | 111 | `directory` |
| `tools/audit_osv.py` | 113 | `binary` |
| `tools/audit_osv.py` | 115 | `url` |
| `tools/audit_osv.py` | 116 | `output` |
| `tools/audit_osv.py` | 116 | `response` |
| `tools/audit_osv.py` | 117 | `chunk` |
| `tools/audit_osv.py` | 122 | `config` |
| `tools/audit_osv.py` | 125 | `expected` |
| `tools/audit_osv.py` | 128 | `report` |
| `tools/audit_osv.py` | 129 | `command` |
| `tools/audit_osv.py` | 139 | `result` |
| `tools/audit_osv.py` | 144 | `scanned` |
| `tools/benchmark.py` | 14 | `main()` |
| `tools/benchmark.py` | 16 | `policy` |
| `tools/benchmark.py` | 17 | `operation` |
| `tools/benchmark.py` | 18 | `original` |
| `tools/benchmark.py` | 19 | `record` |
| `tools/benchmark.py` | 20 | `n` |
| `tools/benchmark.py` | 21 | `n` |
| `tools/benchmark.py` | 22 | `policy` |
| `tools/benchmark.py` | 23 | `operation` |
| `tools/benchmark.py` | 24 | `samples` |
| `tools/benchmark.py` | 25 | `_` |
| `tools/benchmark.py` | 26 | `start` |
| `tools/benchmark.py` | 27 | `result` |
| `tools/browser_server.py` | 16 | `prepare(directory)` |
| `tools/browser_server.py` | 19 | `db` |
| `tools/browser_server.py` | 20 | `credentials` |
| `tools/browser_server.py` | 21 | `store` |
| `tools/browser_server.py` | 24 | `values` |
| `tools/browser_server.py` | 26 | `role` |
| `tools/browser_server.py` | 28 | `entry` |
| `tools/browser_server.py` | 28 | `role` |
| `tools/browser_server.py` | 34 | `main()` |
| `tools/browser_server.py` | 36 | `parser` |
| `tools/browser_server.py` | 39 | `args` |
| `tools/browser_server.py` | 40 | `db` |
| `tools/check_repo.py` | 9 | `main()` |
| `tools/check_repo.py` | 11 | `path` |
| `tools/check_repo.py` | 12 | `relative` |
| `tools/check_repo.py` | 13 | `content` |
| `tools/check_repo.py` | 22 | `ref` |
| `tools/check_repo.py` | 27 | `builtin` |
| `tools/check_repo.py` | 29 | `budget` |
| `tools/check_repo.py` | 29 | `suffix` |
| `tools/check_repo.py` | 30 | `size` |
| `tools/check_repo.py` | 31 | `p` |
| `tools/docs_index.py` | 14 | `ROOT` |
| `tools/docs_index.py` | 15 | `EXCLUDE` |
| `tools/docs_index.py` | 29 | `SPECIAL` |
| `tools/docs_index.py` | 41 | `files()` |
| `tools/docs_index.py` | 43 | `result` |
| `tools/docs_index.py` | 44 | `children` |
| `tools/docs_index.py` | 44 | `directory` |
| `tools/docs_index.py` | 44 | `names` |
| `tools/docs_index.py` | 45 | `child` |
| `tools/docs_index.py` | 46 | `name` |
| `tools/docs_index.py` | 52 | `render()` |
| `tools/docs_index.py` | 54 | `catalog` |
| `tools/docs_index.py` | 62 | `source` |
| `tools/docs_index.py` | 71 | `path` |
| `tools/docs_index.py` | 72 | `relative` |
| `tools/docs_index.py` | 73 | `content` |
| `tools/docs_index.py` | 74 | `description` |
| `tools/docs_index.py` | 77 | `line` |
| `tools/docs_index.py` | 85 | `records` |
| `tools/docs_index.py` | 87 | `node` |
| `tools/docs_index.py` | 89 | `args` |
| `tools/docs_index.py` | 92 | `a` |
| `tools/docs_index.py` | 98 | `line` |
| `tools/docs_index.py` | 98 | `value` |
| `tools/docs_index.py` | 108 | `line` |
| `tools/docs_index.py` | 108 | `value` |
| `tools/docs_index.py` | 111 | `line` |
| `tools/docs_index.py` | 111 | `name` |
| `tools/docs_index.py` | 112 | `node` |
| `tools/docs_index.py` | 126 | `main()` |
| `tools/docs_index.py` | 128 | `content` |
| `tools/docs_index.py` | 128 | `relative` |
| `tools/docs_index.py` | 129 | `path` |
| `tools/fetch_opa.py` | 13 | `ROOT` |
| `tools/fetch_opa.py` | 14 | `VERSION` |
| `tools/fetch_opa.py` | 15 | `RELEASES` |
| `tools/fetch_opa.py` | 39 | `binary()` |
| `tools/fetch_opa.py` | 41 | `checksum` |
| `tools/fetch_opa.py` | 41 | `name` |
| `tools/fetch_opa.py` | 42 | `path` |
| `tools/fetch_opa.py` | 43 | `source` |
| `tools/fetch_opa.py` | 44 | `actual` |
| `tools/fetch_opa.py` | 50 | `main()` |
| `tools/fetch_opa.py` | 52 | `_` |
| `tools/fetch_opa.py` | 52 | `name` |
| `tools/fetch_opa.py` | 53 | `path` |
| `tools/fetch_opa.py` | 60 | `response` |
| `tools/fetch_opa.py` | 61 | `output` |
| `tools/fetch_opa.py` | 63 | `total` |
| `tools/fetch_opa.py` | 64 | `chunk` |
| `tools/fetch_opa.py` | 65 | `total` |
| `tools/fetch_opa.py` | 69 | `path` |
| `tools/opa_checks.py` | 9 | `main()` |
| `tools/opa_checks.py` | 11 | `path` |
| `tools/opa_checks.py` | 12 | `args` |
| `tools/opa_checks.py` | 17 | `completed` |
| `tools/opa_checks.py` | 21 | `report` |
| `tools/opa_checks.py` | 27 | `item` |
| `tools/opa_checks.py` | 27 | `name` |
| `workbench/__main__.py` | 15 | `main()` |
| `workbench/__main__.py` | 17 | `parser` |
| `workbench/__main__.py` | 19 | `commands` |
| `workbench/__main__.py` | 21 | `user` |
| `workbench/__main__.py` | 24 | `serve` |
| `workbench/__main__.py` | 26 | `args` |
| `workbench/__main__.py` | 27 | `store` |
| `workbench/__main__.py` | 32 | `password` |
| `workbench/api.py` | 18 | `HEADERS` |
| `workbench/api.py` | 28 | `create_app(database, port)` |
| `workbench/api.py` | 32 | `origin` |
| `workbench/api.py` | 33 | `authority` |
| `workbench/api.py` | 34 | `app` |
| `workbench/api.py` | 40 | `boundary(request, call_next)` |
| `workbench/api.py` | 42 | `response` |
| `workbench/api.py` | 44 | `response` |
| `workbench/api.py` | 46 | `response` |
| `workbench/api.py` | 52 | `response` |
| `workbench/api.py` | 54 | `response` |
| `workbench/api.py` | 56 | `chunks` |
| `workbench/api.py` | 57 | `size` |
| `workbench/api.py` | 60 | `chunk` |
| `workbench/api.py` | 61 | `size` |
| `workbench/api.py` | 63 | `response` |
| `workbench/api.py` | 71 | `response` |
| `workbench/api.py` | 73 | `response` |
| `workbench/api.py` | 78 | `invalid(_request, error)` |
| `workbench/api.py` | 83 | `e` |
| `workbench/api.py` | 89 | `health()` |
| `workbench/api.py` | 94 | `login(body, request)` |
| `workbench/api.py` | 96 | `token` |
| `workbench/api.py` | 96 | `user` |
| `workbench/api.py` | 97 | `response` |
| `workbench/api.py` | 102 | `me(request)` |
| `workbench/api.py` | 107 | `logout(request)` |
| `workbench/api.py` | 110 | `response` |
| `workbench/api.py` | 115 | `workspace(request)` |
| `workbench/api.py` | 117 | `user` |
| `workbench/api.py` | 118 | `policy` |
| `workbench/api.py` | 118 | `version` |
| `workbench/api.py` | 119 | `audit` |
| `workbench/api.py` | 119 | `history` |
| `workbench/api.py` | 128 | `templates(request)` |
| `workbench/api.py` | 134 | `publish(body, request)` |
| `workbench/api.py` | 136 | `user` |
| `workbench/api.py` | 142 | `assess(body, request)` |
| `workbench/api.py` | 144 | `user` |
| `workbench/api.py` | 145 | `policy` |
| `workbench/api.py` | 145 | `version` |
| `workbench/api.py` | 149 | `result` |
| `workbench/api.py` | 152 | `identifier` |
| `workbench/api.py` | 156 | `report(identifier, request)` |
| `workbench/api.py` | 161 | `review(identifier, body, request)` |
| `workbench/api.py` | 163 | `user` |
| `workbench/api.py` | 168 | `index()` |
| `workbench/auth.py` | 17 | `HASHER` |
| `workbench/auth.py` | 18 | `DUMMY` |
| `workbench/auth.py` | 19 | `VERIFY_GATE` |
| `workbench/auth.py` | 22 | `add_user(store, username, password, role)` |
| `workbench/auth.py` | 32 | `hashed` |
| `workbench/auth.py` | 33 | `db` |
| `workbench/auth.py` | 37 | `sign_in(request, username, password)` |
| `workbench/auth.py` | 39 | `store` |
| `workbench/auth.py` | 40 | `now` |
| `workbench/auth.py` | 41 | `client` |
| `workbench/auth.py` | 44 | `db` |
| `workbench/auth.py` | 46 | `row` |
| `workbench/auth.py` | 55 | `user` |
| `workbench/auth.py` | 66 | `csrf` |
| `workbench/auth.py` | 66 | `token` |
| `workbench/auth.py` | 67 | `db` |
| `workbench/auth.py` | 80 | `identity(request)` |
| `workbench/auth.py` | 82 | `token` |
| `workbench/auth.py` | 85 | `db` |
| `workbench/auth.py` | 86 | `row` |
| `workbench/auth.py` | 95 | `authorize(request, role)` |
| `workbench/auth.py` | 97 | `user` |
| `workbench/auth.py` | 107 | `sign_out(request)` |
| `workbench/auth.py` | 110 | `db` |
| `workbench/engine.py` | 10 | `GATE` |
| `workbench/engine.py` | 11 | `STATUSES` |
| `workbench/engine.py` | 12 | `REASONS` |
| `workbench/engine.py` | 26 | `NOTICE` |
| `workbench/engine.py` | 29 | `EngineUnavailable(class)` |
| `workbench/engine.py` | 33 | `validate_result(value, policy)` |
| `workbench/engine.py` | 41 | `expected` |
| `workbench/engine.py` | 41 | `r` |
| `workbench/engine.py` | 42 | `seen` |
| `workbench/engine.py` | 43 | `row` |
| `workbench/engine.py` | 54 | `row` |
| `workbench/engine.py` | 54 | `statuses` |
| `workbench/engine.py` | 55 | `status` |
| `workbench/engine.py` | 68 | `evaluate(policy, operation)` |
| `workbench/engine.py` | 73 | `command` |
| `workbench/engine.py` | 83 | `completed` |
| `workbench/engine.py` | 96 | `parsed` |
| `workbench/engine.py` | 97 | `value` |
| `workbench/engine.py` | 98 | `result` |
| `workbench/examples.py` | 7 | `FAA` |
| `workbench/examples.py` | 8 | `REMOTE` |
| `workbench/examples.py` | 9 | `PRIVACY` |
| `workbench/examples.py` | 12 | `ORG` |
| `workbench/examples.py` | 15 | `example_policy()` |
| `workbench/examples.py` | 17 | `definitions` |
| `workbench/examples.py` | 127 | `comparator` |
| `workbench/examples.py` | 127 | `condition` |
| `workbench/examples.py` | 127 | `expected` |
| `workbench/examples.py` | 127 | `fact` |
| `workbench/examples.py` | 127 | `identifier` |
| `workbench/examples.py` | 127 | `title` |
| `workbench/examples.py` | 127 | `url` |
| `workbench/examples.py` | 133 | `example_operation()` |
| `workbench/examples.py` | 135 | `values` |
| `workbench/examples.py` | 169 | `fact` |
| `workbench/examples.py` | 169 | `n` |
| `workbench/examples.py` | 169 | `value` |
| `workbench/examples.py` | 175 | `examples()` |
| `workbench/examples.py` | 177 | `baseline` |
| `workbench/examples.py` | 178 | `missing` |
| `workbench/examples.py` | 180 | `e` |
| `workbench/examples.py` | 181 | `privacy` |
| `workbench/examples.py` | 183 | `record` |
| `workbench/examples.py` | 188 | `expired` |
| `workbench/examples.py` | 190 | `record` |
| `workbench/models.py` | 16 | `Label` |
| `workbench/models.py` | 17 | `Key` |
| `workbench/models.py` | 35 | `NUMERIC` |
| `workbench/models.py` | 36 | `Value` |
| `workbench/models.py` | 37 | `Clock` |
| `workbench/models.py` | 40 | `valid_value(key, value)` |
| `workbench/models.py` | 51 | `Contract(class)` |
| `workbench/models.py` | 54 | `model_config` |
| `workbench/models.py` | 57 | `Evidence(class)` |
| `workbench/models.py` | 60 | `id` |
| `workbench/models.py` | 61 | `fact` |
| `workbench/models.py` | 62 | `value` |
| `workbench/models.py` | 63 | `source_ref` |
| `workbench/models.py` | 64 | `observed_s` |
| `workbench/models.py` | 65 | `expires_s` |
| `workbench/models.py` | 66 | `attested` |
| `workbench/models.py` | 69 | `coherent(self)` |
| `workbench/models.py` | 77 | `Rule(class)` |
| `workbench/models.py` | 80 | `id` |
| `workbench/models.py` | 81 | `title` |
| `workbench/models.py` | 82 | `fact` |
| `workbench/models.py` | 83 | `comparator` |
| `workbench/models.py` | 84 | `expected` |
| `workbench/models.py` | 85 | `max_age_s` |
| `workbench/models.py` | 86 | `when_fact` |
| `workbench/models.py` | 87 | `when_value` |
| `workbench/models.py` | 88 | `source_url` |
| `workbench/models.py` | 94 | `reference` |
| `workbench/models.py` | 97 | `typed(self)` |
| `workbench/models.py` | 109 | `Policy(class)` |
| `workbench/models.py` | 112 | `name` |
| `workbench/models.py` | 113 | `jurisdiction` |
| `workbench/models.py` | 114 | `framework` |
| `workbench/models.py` | 115 | `valid_from_s` |
| `workbench/models.py` | 116 | `valid_until_s` |
| `workbench/models.py` | 117 | `rules` |
| `workbench/models.py` | 120 | `consistent(self)` |
| `workbench/models.py` | 122 | `r` |
| `workbench/models.py` | 126 | `a` |
| `workbench/models.py` | 126 | `i` |
| `workbench/models.py` | 127 | `b` |
| `workbench/models.py` | 139 | `lo` |
| `workbench/models.py` | 140 | `r` |
| `workbench/models.py` | 141 | `r` |
| `workbench/models.py` | 144 | `hi` |
| `workbench/models.py` | 145 | `r` |
| `workbench/models.py` | 146 | `r` |
| `workbench/models.py` | 154 | `Operation(class)` |
| `workbench/models.py` | 157 | `name` |
| `workbench/models.py` | 158 | `jurisdiction` |
| `workbench/models.py` | 159 | `framework` |
| `workbench/models.py` | 160 | `as_of_s` |
| `workbench/models.py` | 161 | `evidence` |
| `workbench/models.py` | 164 | `unique(self)` |
| `workbench/models.py` | 166 | `e` |
| `workbench/models.py` | 171 | `Login(class)` |
| `workbench/models.py` | 174 | `username` |
| `workbench/models.py` | 175 | `password` |
| `workbench/models.py` | 178 | `Evaluate(class)` |
| `workbench/models.py` | 181 | `version` |
| `workbench/models.py` | 182 | `operation` |
| `workbench/models.py` | 185 | `Publish(class)` |
| `workbench/models.py` | 188 | `expected_version` |
| `workbench/models.py` | 189 | `policy` |
| `workbench/models.py` | 192 | `Review(class)` |
| `workbench/models.py` | 195 | `decision` |
| `workbench/models.py` | 196 | `note` |
| `workbench/schema.sql` | 3 | `PRAGMA foreign_keys = ON;` |
| `workbench/schema.sql` | 4 | `CREATE TABLE IF NOT EXISTS users (` |
| `workbench/schema.sql` | 5 | `name TEXT PRIMARY KEY, password_hash TEXT NOT NULL,` |
| `workbench/schema.sql` | 6 | `role TEXT NOT NULL CHECK(role IN ('admin','operator','reviewer'))` |
| `workbench/schema.sql` | 7 | `);` |
| `workbench/schema.sql` | 8 | `CREATE TABLE IF NOT EXISTS sessions (` |
| `workbench/schema.sql` | 9 | `digest TEXT PRIMARY KEY, username TEXT NOT NULL REFERENCES users(name),` |
| `workbench/schema.sql` | 10 | `csrf TEXT NOT NULL, expires REAL NOT NULL, created REAL NOT NULL` |
| `workbench/schema.sql` | 11 | `);` |
| `workbench/schema.sql` | 12 | `CREATE INDEX IF NOT EXISTS sessions_user ON sessions(username);` |
| `workbench/schema.sql` | 13 | `CREATE TABLE IF NOT EXISTS attempts (client TEXT PRIMARY KEY, count INTEGER NOT NULL, started REAL NOT NULL);` |
| `workbench/schema.sql` | 14 | `CREATE TABLE IF NOT EXISTS policies (` |
| `workbench/schema.sql` | 15 | `version INTEGER PRIMARY KEY, content TEXT NOT NULL, digest TEXT NOT NULL, actor TEXT NOT NULL, created TEXT NOT NULL` |
| `workbench/schema.sql` | 16 | `);` |
| `workbench/schema.sql` | 17 | `CREATE TABLE IF NOT EXISTS workspace (id INTEGER PRIMARY KEY CHECK(id=1), active_version INTEGER NOT NULL REFERENCES policies(version), schema_version INTEGER NOT NULL CHECK(schema_version=1));` |
| `workbench/schema.sql` | 18 | `CREATE TABLE IF NOT EXISTS evaluations (` |
| `workbench/schema.sql` | 19 | `id INTEGER PRIMARY KEY, version INTEGER NOT NULL REFERENCES policies(version), creator TEXT NOT NULL REFERENCES users(name),` |
| `workbench/schema.sql` | 20 | `operation TEXT NOT NULL, result TEXT NOT NULL, digest TEXT NOT NULL, created TEXT NOT NULL` |
| `workbench/schema.sql` | 21 | `);` |
| `workbench/schema.sql` | 22 | `CREATE TABLE IF NOT EXISTS reviews (` |
| `workbench/schema.sql` | 23 | `evaluation INTEGER PRIMARY KEY REFERENCES evaluations(id), actor TEXT NOT NULL REFERENCES users(name),` |
| `workbench/schema.sql` | 24 | `decision TEXT NOT NULL CHECK(decision IN ('acknowledge','reject')), note TEXT NOT NULL, created TEXT NOT NULL` |
| `workbench/schema.sql` | 25 | `);` |
| `workbench/schema.sql` | 26 | `CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, at TEXT NOT NULL, actor TEXT NOT NULL, event TEXT NOT NULL, version INTEGER NOT NULL, detail TEXT NOT NULL);` |
| `workbench/schema.sql` | 27 | `CREATE INDEX IF NOT EXISTS evaluations_creator ON evaluations(creator,id DESC);` |
| `workbench/schema.sql` | 28 | `CREATE TRIGGER IF NOT EXISTS immutable_policy_update BEFORE UPDATE ON policies BEGIN SELECT RAISE(ABORT,'immutable policy'); END;` |
| `workbench/schema.sql` | 29 | `CREATE TRIGGER IF NOT EXISTS immutable_policy_delete BEFORE DELETE ON policies BEGIN SELECT RAISE(ABORT,'immutable policy'); END;` |
| `workbench/schema.sql` | 30 | `CREATE TRIGGER IF NOT EXISTS immutable_evaluation_update BEFORE UPDATE ON evaluations BEGIN SELECT RAISE(ABORT,'immutable evaluation'); END;` |
| `workbench/schema.sql` | 31 | `CREATE TRIGGER IF NOT EXISTS immutable_evaluation_delete BEFORE DELETE ON evaluations BEGIN SELECT RAISE(ABORT,'immutable evaluation'); END;` |
| `workbench/schema.sql` | 32 | `CREATE TRIGGER IF NOT EXISTS immutable_review_update BEFORE UPDATE ON reviews BEGIN SELECT RAISE(ABORT,'immutable review'); END;` |
| `workbench/schema.sql` | 33 | `CREATE TRIGGER IF NOT EXISTS immutable_review_delete BEFORE DELETE ON reviews BEGIN SELECT RAISE(ABORT,'immutable review'); END;` |
| `workbench/store.py` | 15 | `canonical(value)` |
| `workbench/store.py` | 20 | `digest(value)` |
| `workbench/store.py` | 25 | `now()` |
| `workbench/store.py` | 30 | `Store(class)` |
| `workbench/store.py` | 33 | `__init__(self, path)` |
| `workbench/store.py` | 37 | `db` |
| `workbench/store.py` | 41 | `connect(self, write)` |
| `workbench/store.py` | 43 | `db` |
| `workbench/store.py` | 55 | `event(self, db, actor, event, version, detail)` |
| `workbench/store.py` | 62 | `initialize(self, policy)` |
| `workbench/store.py` | 64 | `db` |
| `workbench/store.py` | 74 | `snapshot(self, db)` |
| `workbench/store.py` | 77 | `connection` |
| `workbench/store.py` | 79 | `row` |
| `workbench/store.py` | 84 | `policy` |
| `workbench/store.py` | 89 | `publish(self, expected, policy, actor)` |
| `workbench/store.py` | 91 | `db` |
| `workbench/store.py` | 92 | `_` |
| `workbench/store.py` | 92 | `version` |
| `workbench/store.py` | 95 | `version` |
| `workbench/store.py` | 104 | `save(self, version, operation, result, actor)` |
| `workbench/store.py` | 106 | `db` |
| `workbench/store.py` | 107 | `active` |
| `workbench/store.py` | 107 | `policy` |
| `workbench/store.py` | 110 | `content` |
| `workbench/store.py` | 116 | `cursor` |
| `workbench/store.py` | 130 | `get(self, identifier, user, db)` |
| `workbench/store.py` | 133 | `connection` |
| `workbench/store.py` | 135 | `row` |
| `workbench/store.py` | 141 | `result` |
| `workbench/store.py` | 142 | `key` |
| `workbench/store.py` | 145 | `key` |
| `workbench/store.py` | 149 | `_` |
| `workbench/store.py` | 149 | `active` |
| `workbench/store.py` | 151 | `review` |
| `workbench/store.py` | 158 | `review(self, identifier, user, decision, note)` |
| `workbench/store.py` | 160 | `db` |
| `workbench/store.py` | 161 | `report` |
| `workbench/store.py` | 182 | `history(self, user)` |
| `workbench/store.py` | 184 | `db` |
| `workbench/store.py` | 186 | `rows` |
| `workbench/store.py` | 190 | `events` |
| `workbench/store.py` | 192 | `rows` |
| `workbench/store.py` | 195 | `events` |
| `workbench/store.py` | 196 | `r` |
| `workbench/store.py` | 198 | `r` |
| `ui/src/main.ts` | 12 | `Rule` |
| `ui/src/main.ts` | 22 | `Policy` |
| `ui/src/main.ts` | 26 | `Workspace` |
| `ui/src/main.ts` | 32 | `root` |
| `ui/src/main.ts` | 47 | `el` |
| `ui/src/main.ts` | 47 | `id` |
| `ui/src/main.ts` | 51 | `text` |
| `ui/src/main.ts` | 51 | `tag` |
| `ui/src/main.ts` | 51 | `value` |
| `ui/src/main.ts` | 52 | `node` |
| `ui/src/main.ts` | 56 | `user` |
| `ui/src/main.ts` | 57 | `workspace` |
| `ui/src/main.ts` | 58 | `report` |
| `ui/src/main.ts` | 59 | `templates` |
| `ui/src/main.ts` | 60 | `revision` |
| `ui/src/main.ts` | 61 | `policyDraftVersion` |
| `ui/src/main.ts` | 62 | `busy` |
| `ui/src/main.ts` | 64 | `api` |
| `ui/src/main.ts` | 64 | `path` |
| `ui/src/main.ts` | 64 | `body` |
| `ui/src/main.ts` | 65 | `response` |
| `ui/src/main.ts` | 77 | `result` |
| `ui/src/main.ts` | 82 | `invalidate` |
| `ui/src/main.ts` | 97 | `action` |
| `ui/src/main.ts` | 97 | `task` |
| `ui/src/main.ts` | 102 | `id` |
| `ui/src/main.ts` | 106 | `error` |
| `ui/src/main.ts` | 115 | `permissions` |
| `ui/src/main.ts` | 133 | `refresh` |
| `ui/src/main.ts` | 133 | `preserveDraft` |
| `ui/src/main.ts` | 152 | `item` |
| `ui/src/main.ts` | 153 | `node` |
| `ui/src/main.ts` | 154 | `button` |
| `ui/src/main.ts` | 173 | `item` |
| `ui/src/main.ts` | 186 | `renderReport` |
| `ui/src/main.ts` | 188 | `result` |
| `ui/src/main.ts` | 189 | `summary` |
| `ui/src/main.ts` | 202 | `policy` |
| `ui/src/main.ts` | 203 | `check` |
| `ui/src/main.ts` | 204 | `rule` |
| `ui/src/main.ts` | 204 | `r` |
| `ui/src/main.ts` | 205 | `row` |
| `ui/src/main.ts` | 211 | `source` |
| `ui/src/main.ts` | 212 | `link` |
| `ui/src/main.ts` | 222 | `loadReport` |
| `ui/src/main.ts` | 223 | `identifier` |
| `ui/src/main.ts` | 224 | `requested` |
| `ui/src/main.ts` | 226 | `selected` |
| `ui/src/main.ts` | 237 | `signedIn` |
| `ui/src/main.ts` | 252 | `event` |
| `ui/src/main.ts` | 276 | `node` |
| `ui/src/main.ts` | 287 | `requested` |
| `ui/src/main.ts` | 288 | `operation` |
| `ui/src/main.ts` | 289 | `result` |
| `ui/src/main.ts` | 309 | `requested` |
| `ui/src/main.ts` | 310 | `published` |
| `ui/src/main.ts` | 332 | `[id, decision]` |
| `ui/src/main.ts` | 340 | `identifier` |
| `ui/src/main.ts` | 341 | `requested` |
| `ui/src/main.ts` | 346 | `loaded` |
| `ui/src/main.ts` | 373 | `url` |
| `ui/src/main.ts` | 376 | `link` |
| `ui/src/view.test.ts` | 11 | `user` |
| `ui/src/view.test.ts` | 12 | `report` |
| `ui/src/view.test.ts` | 32 | `status` |
| `ui/src/view.ts` | 3 | `User` |
| `ui/src/view.ts` | 8 | `Check` |
| `ui/src/view.ts` | 13 | `Result` |
| `ui/src/view.ts` | 19 | `Report` |
| `ui/src/view.ts` | 32 | `statusLabel` |
| `ui/src/view.ts` | 32 | `status` |
| `ui/src/view.ts` | 40 | `reasonLabel` |
| `ui/src/view.ts` | 40 | `reason` |
| `ui/src/view.ts` | 44 | `canReview` |
| `ui/src/view.ts` | 45 | `user` |
| `ui/src/view.ts` | 46 | `report` |
| `ui/src/view.ts` | 47 | `acknowledge` |
| `ui/src/view.ts` | 58 | `counts` |
| `ui/src/view.ts` | 58 | `checks` |
| `ui/src/view.ts` | 60 | `sum` |
| `ui/src/view.ts` | 60 | `row` |
| `tests/browser/workbench.spec.ts` | 6 | `login` |
| `tests/browser/workbench.spec.ts` | 6 | `page` |
| `tests/browser/workbench.spec.ts` | 6 | `role` |
| `tests/browser/workbench.spec.ts` | 7 | `credentials` |
| `tests/browser/workbench.spec.ts` | 19 | `{ page, }` |
| `tests/browser/workbench.spec.ts` | 32 | `download` |
| `tests/browser/workbench.spec.ts` | 37 | `[value, label]` |
| `tests/browser/workbench.spec.ts` | 58 | `changed` |
| `tests/browser/workbench.spec.ts` | 60 | `releaseReport` |
| `tests/browser/workbench.spec.ts` | 61 | `enteredReport` |
| `tests/browser/workbench.spec.ts` | 62 | `reportStarted` |
| `tests/browser/workbench.spec.ts` | 62 | `resolve` |
| `tests/browser/workbench.spec.ts` | 65 | `reportGate` |
| `tests/browser/workbench.spec.ts` | 65 | `resolve` |
| `tests/browser/workbench.spec.ts` | 70 | `route` |
| `tests/browser/workbench.spec.ts` | 90 | `{ page, }` |
| `tests/browser/workbench.spec.ts` | 96 | `historyButton` |
| `tests/browser/workbench.spec.ts` | 100 | `policy` |
| `tests/browser/workbench.spec.ts` | 111 | `currentReport` |
| `tests/browser/workbench.spec.ts` | 139 | `operatorReport` |
| `tests/browser/workbench.spec.ts` | 163 | `{ page, }` |
| `tests/browser/workbench.spec.ts` | 167 | `release` |
| `tests/browser/workbench.spec.ts` | 168 | `entered` |
| `tests/browser/workbench.spec.ts` | 169 | `started` |
| `tests/browser/workbench.spec.ts` | 169 | `resolve` |
| `tests/browser/workbench.spec.ts` | 172 | `gate` |
| `tests/browser/workbench.spec.ts` | 172 | `resolve` |
| `tests/browser/workbench.spec.ts` | 177 | `route` |
| `tests/browser/workbench.spec.ts` | 186 | `changed` |
| `tools/source_index.mjs` | 7 | `collect` |
| `tools/source_index.mjs` | 7 | `root` |
| `tools/source_index.mjs` | 10 | `a` |
| `tools/source_index.mjs` | 10 | `b` |
| `tools/source_index.mjs` | 11 | `entry` |
| `tools/source_index.mjs` | 12 | `name` |
| `tools/source_index.mjs` | 20 | `file` |
| `tools/source_index.mjs` | 23 | `name` |
| `tools/source_index.mjs` | 27 | `source` |
| `tools/source_index.mjs` | 33 | `records` |
| `tools/source_index.mjs` | 35 | `visit` |
| `tools/source_index.mjs` | 35 | `node` |
| `tools/source_index.mjs` | 44 | `name` |
| `tools/source_index.mjs` | 48 | `line` |
| `tools/source_index.mjs` | 59 | `row` |
| `playwright.config.ts` | 5 | `directory` |
| `playwright.config.ts` | 8 | `local` |
| `playwright.config.ts` | 12 | `python` |
