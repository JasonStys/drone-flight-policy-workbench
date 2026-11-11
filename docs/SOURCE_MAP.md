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
| `tests/runtime_notice_cases.py` | 10 | `ROOT` |
| `tests/runtime_notice_cases.py` | 14 | `interpreter()` |
| `tests/runtime_notice_cases.py` | 16 | `root` |
| `tests/runtime_notice_cases.py` | 24 | `test_actual_tcl_notice_reader_preserves_bytes_and_missing_identity(tmp_path, interpreter)` |
| `tests/runtime_notice_cases.py` | 26 | `path` |
| `tests/runtime_notice_cases.py` | 27 | `raw` |
| `tests/runtime_notice_cases.py` | 34 | `raw` |
| `tests/runtime_notice_cases.py` | 42 | `test_exact_mac_version_uses_verbatim_upstream_notice_and_binds_digest(tmp_path, kind, interpreter)` |
| `tests/runtime_notice_cases.py` | 46 | `library` |
| `tests/runtime_notice_cases.py` | 47 | `file` |
| `tests/runtime_notice_cases.py` | 48 | `target` |
| `tests/runtime_notice_cases.py` | 51 | `raw` |
| `tests/runtime_notice_cases.py` | 51 | `source` |
| `tests/runtime_notice_cases.py` | 78 | `test_unreviewed_platform_version_or_library_cannot_substitute_notice(version, library, system, interpreter)` |
| `tests/runtime_notice_cases.py` | 87 | `test_ubuntu_uses_actual_runtime_package_copyright_not_guessed_script_file(tmp_path, monkeypatch, kind, interpreter)` |
| `tests/runtime_notice_cases.py` | 91 | `fixture` |
| `tests/runtime_notice_cases.py` | 93 | `actual` |
| `tests/runtime_notice_cases.py` | 94 | `calls` |
| `tests/runtime_notice_cases.py` | 95 | `library` |
| `tests/runtime_notice_cases.py` | 96 | `package_path` |
| `tests/runtime_notice_cases.py` | 98 | `installed(interpreter, path)` |
| `tests/runtime_notice_cases.py` | 105 | `raw` |
| `tests/runtime_notice_cases.py` | 105 | `source` |
| `tests/runtime_notice_cases.py` | 110 | `test_present_invalid_runtime_notice_never_falls_back_to_other_terms(tmp_path, interpreter)` |
| `tests/runtime_notice_cases.py` | 118 | `test_mac_pre905_terms_require_exact_psf_sdk_recipe(tmp_path, monkeypatch, interpreter, python_version, accepted)` |
| `tests/runtime_notice_cases.py` | 123 | `library` |
| `tests/runtime_notice_cases.py` | 124 | `name` |
| `tests/runtime_notice_cases.py` | 128 | `raw` |
| `tests/runtime_notice_cases.py` | 128 | `source` |
| `tests/runtime_notice_cases.py` | 136 | `test_mac_pre905_changed_notice_is_rejected(tmp_path, monkeypatch, interpreter)` |
| `tests/runtime_notice_cases.py` | 140 | `path` |
| `tests/runtime_notice_cases.py` | 142 | `library` |
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
| `tests/test_api_store.py` | 55 | `test_admin_policy_preview_roles_csrf_no_mutation_stale_and_engine_failure(application, monkeypatch)` |
| `tests/test_api_store.py` | 59 | `admin` |
| `tests/test_api_store.py` | 60 | `original` |
| `tests/test_api_store.py` | 61 | `body` |
| `tests/test_api_store.py` | 66 | `endpoint` |
| `tests/test_api_store.py` | 67 | `name` |
| `tests/test_api_store.py` | 69 | `csrf` |
| `tests/test_api_store.py` | 72 | `response` |
| `tests/test_api_store.py` | 79 | `unavailable()` |
| `tests/test_api_store.py` | 87 | `concurrent()` |
| `tests/test_api_store.py` | 89 | `result` |
| `tests/test_api_store.py` | 97 | `test_end_to_end_independent_acknowledgement(application)` |
| `tests/test_api_store.py` | 99 | `operator` |
| `tests/test_api_store.py` | 100 | `reviewer` |
| `tests/test_api_store.py` | 101 | `response` |
| `tests/test_api_store.py` | 103 | `identifier` |
| `tests/test_api_store.py` | 104 | `report` |
| `tests/test_api_store.py` | 110 | `reviewed` |
| `tests/test_api_store.py` | 132 | `test_private_objects_and_roles(application)` |
| `tests/test_api_store.py` | 134 | `operator` |
| `tests/test_api_store.py` | 135 | `other` |
| `tests/test_api_store.py` | 136 | `admin` |
| `tests/test_api_store.py` | 137 | `identifier` |
| `tests/test_api_store.py` | 143 | `payload` |
| `tests/test_api_store.py` | 165 | `test_self_review_and_holds(application)` |
| `tests/test_api_store.py` | 167 | `reviewer` |
| `tests/test_api_store.py` | 168 | `operator` |
| `tests/test_api_store.py` | 169 | `own` |
| `tests/test_api_store.py` | 176 | `status` |
| `tests/test_api_store.py` | 177 | `operation` |
| `tests/test_api_store.py` | 179 | `identifier` |
| `tests/test_api_store.py` | 196 | `test_origin_csrf_size_and_headers(application)` |
| `tests/test_api_store.py` | 198 | `value` |
| `tests/test_api_store.py` | 217 | `invalid` |
| `tests/test_api_store.py` | 227 | `test_login_expiry_revocation_and_hashes(application)` |
| `tests/test_api_store.py` | 229 | `value` |
| `tests/test_api_store.py` | 230 | `token` |
| `tests/test_api_store.py` | 232 | `db` |
| `tests/test_api_store.py` | 241 | `value` |
| `tests/test_api_store.py` | 242 | `db` |
| `tests/test_api_store.py` | 250 | `test_login_failures_throttle_and_cookie(application)` |
| `tests/test_api_store.py` | 252 | `value` |
| `tests/test_api_store.py` | 253 | `name` |
| `tests/test_api_store.py` | 262 | `response` |
| `tests/test_api_store.py` | 271 | `db` |
| `tests/test_api_store.py` | 291 | `test_provisioning_rejects_invalid(application, name, password, role)` |
| `tests/test_api_store.py` | 297 | `test_session_limit_attempt_capacity_and_cleanup(application)` |
| `tests/test_api_store.py` | 299 | `store` |
| `tests/test_api_store.py` | 300 | `db` |
| `tests/test_api_store.py` | 301 | `n` |
| `tests/test_api_store.py` | 308 | `db` |
| `tests/test_api_store.py` | 313 | `db` |
| `tests/test_api_store.py` | 315 | `n` |
| `tests/test_api_store.py` | 317 | `value` |
| `tests/test_api_store.py` | 328 | `test_engine_and_stale_persistence(application, monkeypatch)` |
| `tests/test_api_store.py` | 330 | `value` |
| `tests/test_api_store.py` | 332 | `fail()` |
| `tests/test_api_store.py` | 339 | `concurrent(policy, operation)` |
| `tests/test_api_store.py` | 349 | `test_atomic_version_race_and_immutable_rows(application)` |
| `tests/test_api_store.py` | 351 | `store` |
| `tests/test_api_store.py` | 353 | `publish()` |
| `tests/test_api_store.py` | 360 | `pool` |
| `tests/test_api_store.py` | 364 | `user` |
| `tests/test_api_store.py` | 365 | `identifier` |
| `tests/test_api_store.py` | 367 | `statement` |
| `tests/test_api_store.py` | 375 | `db` |
| `tests/test_api_store.py` | 380 | `test_corruption_missing_install_and_slow_body(application, tmp_path, monkeypatch)` |
| `tests/test_api_store.py` | 382 | `empty` |
| `tests/test_api_store.py` | 385 | `db` |
| `tests/test_api_store.py` | 393 | `Timeout(class)` |
| `tests/test_api_store.py` | 396 | `__aenter__(self)` |
| `tests/test_api_store.py` | 399 | `__aexit__(self)` |
| `tests/test_api_store.py` | 411 | `test_evaluation_corruption(application)` |
| `tests/test_api_store.py` | 413 | `value` |
| `tests/test_api_store.py` | 414 | `identifier` |
| `tests/test_api_store.py` | 415 | `db` |
| `tests/test_api_store.py` | 421 | `test_origin_port_validation()` |
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
| `tests/test_current_installed_guide.py` | 10 | `test_current_edition_exposes_document_and_relationships(tmp_path, monkeypatch)` |
| `tests/test_current_installed_guide.py` | 14 | `current` |
| `tests/test_current_installed_guide.py` | 16 | `package` |
| `tests/test_current_installed_guide.py` | 25 | `content` |
| `tests/test_current_installed_guide.py` | 28 | `unknown` |
| `tests/test_desktop_host.py` | 15 | `prepared(tmp_path)` |
| `tests/test_desktop_host.py` | 17 | `profile` |
| `tests/test_desktop_host.py` | 24 | `request(host, path)` |
| `tests/test_desktop_host.py` | 26 | `connection` |
| `tests/test_desktop_host.py` | 31 | `response` |
| `tests/test_desktop_host.py` | 37 | `test_actual_readiness_private_login_and_owned_stop(tmp_path)` |
| `tests/test_desktop_host.py` | 39 | `profile` |
| `tests/test_desktop_host.py` | 40 | `metadata` |
| `tests/test_desktop_host.py` | 41 | `host` |
| `tests/test_desktop_host.py` | 44 | `_` |
| `tests/test_desktop_host.py` | 44 | `code` |
| `tests/test_desktop_host.py` | 44 | `raw` |
| `tests/test_desktop_host.py` | 45 | `health` |
| `tests/test_desktop_host.py` | 50 | `login` |
| `tests/test_desktop_host.py` | 61 | `code` |
| `tests/test_desktop_host.py` | 61 | `headers` |
| `tests/test_desktop_host.py` | 61 | `raw` |
| `tests/test_desktop_host.py` | 69 | `cookie` |
| `tests/test_desktop_host.py` | 89 | `test_actual_partial_body_bounds_pre_shutdown_drain(tmp_path)` |
| `tests/test_desktop_host.py` | 91 | `profile` |
| `tests/test_desktop_host.py` | 92 | `host` |
| `tests/test_desktop_host.py` | 93 | `received` |
| `tests/test_desktop_host.py` | 95 | `ObserveRead(class)` |
| `tests/test_desktop_host.py` | 98 | `__init__(self, app)` |
| `tests/test_desktop_host.py` | 101 | `__call__(self, scope, receive, send)` |
| `tests/test_desktop_host.py` | 102 | `observed()` |
| `tests/test_desktop_host.py` | 103 | `message` |
| `tests/test_desktop_host.py` | 113 | `connection` |
| `tests/test_desktop_host.py` | 124 | `response` |
| `tests/test_desktop_host.py` | 140 | `test_startup_failure_is_never_reported_as_ready(tmp_path, monkeypatch, failure)` |
| `tests/test_desktop_host.py` | 142 | `profile` |
| `tests/test_desktop_host.py` | 143 | `host` |
| `tests/test_desktop_host.py` | 145 | `broken()` |
| `tests/test_desktop_host.py` | 163 | `test_two_actual_profiles_keep_sessions_in_one_host_scoped_cookie_jar(tmp_path)` |
| `tests/test_desktop_host.py` | 165 | `first` |
| `tests/test_desktop_host.py` | 166 | `second` |
| `tests/test_desktop_host.py` | 167 | `password` |
| `tests/test_desktop_host.py` | 171 | `hosts` |
| `tests/test_desktop_host.py` | 173 | `host` |
| `tests/test_desktop_host.py` | 175 | `client` |
| `tests/test_desktop_host.py` | 176 | `host` |
| `tests/test_desktop_host.py` | 176 | `name` |
| `tests/test_desktop_host.py` | 177 | `response` |
| `tests/test_desktop_host.py` | 183 | `cookie` |
| `tests/test_desktop_host.py` | 187 | `host` |
| `tests/test_desktop_host.py` | 187 | `users` |
| `tests/test_desktop_host.py` | 188 | `user` |
| `tests/test_desktop_host.py` | 189 | `foreign_cookie` |
| `tests/test_desktop_host.py` | 196 | `wrong_csrf` |
| `tests/test_desktop_host.py` | 213 | `host` |
| `tests/test_desktop_host.py` | 220 | `test_invalid_cookie_namespace_is_rejected_before_database_creation(tmp_path, invalid)` |
| `tests/test_desktop_host.py` | 224 | `database` |
| `tests/test_desktop_package.py` | 15 | `test_collected_vendor_bytes_and_mode_are_restored_without_reblessing_digest(tmp_path)` |
| `tests/test_desktop_package.py` | 17 | `source` |
| `tests/test_desktop_package.py` | 20 | `expected` |
| `tests/test_desktop_package.py` | 21 | `bundle` |
| `tests/test_desktop_package.py` | 22 | `target` |
| `tests/test_desktop_package.py` | 25 | `result` |
| `tests/test_desktop_package.py` | 34 | `before` |
| `tests/test_desktop_package.py` | 40 | `test_missing_noncanonical_or_unowned_vendor_paths_cannot_be_created(tmp_path)` |
| `tests/test_desktop_package.py` | 42 | `source` |
| `tests/test_desktop_package.py` | 44 | `expected` |
| `tests/test_desktop_package.py` | 45 | `bundle` |
| `tests/test_desktop_package.py` | 68 | `test_freeze_refuses_old_cached_or_prerelease_runtime(version, level, allowed)` |
| `tests/test_desktop_package.py` | 73 | `test_all_product_version_surfaces_agree()` |
| `tests/test_desktop_package.py` | 84 | `test_mismatched_version_or_identity_cannot_build(tmp_path, surface)` |
| `tests/test_desktop_package.py` | 86 | `root` |
| `tests/test_desktop_package.py` | 87 | `path` |
| `tests/test_desktop_package.py` | 88 | `output` |
| `tests/test_desktop_package.py` | 91 | `selected` |
| `tests/test_desktop_package.py` | 99 | `path` |
| `tests/test_desktop_package.py` | 103 | `value` |
| `tests/test_desktop_package.py` | 127 | `test_source_cleanliness_is_not_a_release_flag_waiver(monkeypatch, dirty, ci, override, sha, allowed)` |
| `tests/test_desktop_package.py` | 132 | `output(command)` |
| `tests/test_desktop_package.py` | 149 | `value` |
| `tests/test_desktop_package.py` | 153 | `test_archive_rejection_remains_active_with_optimized_python()` |
| `tests/test_desktop_package.py` | 155 | `result` |
| `tests/test_desktop_profile.py` | 13 | `database_snapshot(store)` |
| `tests/test_desktop_profile.py` | 15 | `database` |
| `tests/test_desktop_profile.py` | 19 | `test_provision_persist_login_and_existing_roles(tmp_path)` |
| `tests/test_desktop_profile.py` | 21 | `path` |
| `tests/test_desktop_profile.py` | 22 | `profile` |
| `tests/test_desktop_profile.py` | 30 | `original` |
| `tests/test_desktop_profile.py` | 31 | `namespace` |
| `tests/test_desktop_profile.py` | 32 | `marker_bytes` |
| `tests/test_desktop_profile.py` | 39 | `reopened` |
| `tests/test_desktop_profile.py` | 46 | `client` |
| `tests/test_desktop_profile.py` | 48 | `response` |
| `tests/test_desktop_profile.py` | 54 | `db` |
| `tests/test_desktop_profile.py` | 55 | `row` |
| `tests/test_desktop_profile.py` | 55 | `values` |
| `tests/test_desktop_profile.py` | 56 | `value` |
| `tests/test_desktop_profile.py` | 61 | `test_invalid_duplicate_and_first_role_do_not_create_account(tmp_path)` |
| `tests/test_desktop_profile.py` | 63 | `profile` |
| `tests/test_desktop_profile.py` | 65 | `args` |
| `tests/test_desktop_profile.py` | 74 | `db` |
| `tests/test_desktop_profile.py` | 75 | `original_hash` |
| `tests/test_desktop_profile.py` | 83 | `db` |
| `tests/test_desktop_profile.py` | 104 | `test_invalid_marker_never_adopts_unknown_profile(tmp_path, content)` |
| `tests/test_desktop_profile.py` | 106 | `folder` |
| `tests/test_desktop_profile.py` | 114 | `test_unknown_folder_and_wrong_product_are_preserved(tmp_path)` |
| `tests/test_desktop_profile.py` | 116 | `important` |
| `tests/test_desktop_profile.py` | 125 | `marker` |
| `tests/test_desktop_profile.py` | 131 | `test_default_directory_is_per_user_and_outside_source(monkeypatch, tmp_path)` |
| `tests/test_desktop_resources.py` | 13 | `test_source_mode_is_explicit_and_frozen_missing_identity_fails(tmp_path, monkeypatch)` |
| `tests/test_desktop_resources.py` | 36 | `test_each_wrong_frozen_identity_surface_is_rejected(tmp_path, field, value)` |
| `tests/test_desktop_resources.py` | 38 | `path` |
| `tests/test_desktop_resources.py` | 40 | `valid` |
| `tests/test_desktop_resources.py` | 55 | `test_resources_are_real_regular_nonempty_bounded_files(tmp_path)` |
| `tests/test_desktop_resources.py` | 57 | `path` |
| `tests/test_desktop_resources.py` | 60 | `raw` |
| `tests/test_desktop_resources.py` | 68 | `test_console_owner_uses_actual_saved_profile_and_quits_without_password_input(tmp_path, monkeypatch, capsys)` |
| `tests/test_desktop_resources.py` | 74 | `path` |
| `tests/test_desktop_resources.py` | 75 | `profile` |
| `tests/test_desktop_resources.py` | 82 | `output` |
| `tests/test_desktop_resources.py` | 85 | `reopened` |
| `tests/test_desktop_resources.py` | 92 | `test_console_cannot_create_preset_first_account(tmp_path)` |
| `tests/test_desktop_resources.py` | 96 | `path` |
| `tests/test_desktop_resources.py` | 99 | `profile` |
| `tests/test_desktop_resources.py` | 106 | `test_entrypoint_requires_explicit_console_mode_and_real_resources(tmp_path, monkeypatch, capsys)` |
| `tests/test_desktop_resources.py` | 110 | `error` |
| `tests/test_desktop_resources.py` | 121 | `test_normal_entrypoint_presents_native_controls(tmp_path, monkeypatch)` |
| `tests/test_desktop_resources.py` | 125 | `observed` |
| `tests/test_desktop_resources.py` | 127 | `close_after_construct(root, directory, metadata)` |
| `tests/test_desktop_resources.py` | 141 | `test_actual_loaded_tk_matches_package_and_runtime_info_opens_no_profile(tmp_path, monkeypatch, capsys)` |
| `tests/test_desktop_resources.py` | 147 | `root` |
| `tests/test_desktop_resources.py` | 150 | `versions` |
| `tests/test_desktop_resources.py` | 159 | `_` |
| `tests/test_desktop_resources.py` | 162 | `output` |
| `tests/test_desktop_resources.py` | 163 | `record` |
| `tests/test_desktop_resources.py` | 164 | `name` |
| `tests/test_desktop_resources.py` | 168 | `test_console_interrupt_drains_the_actual_owned_host_and_releases_profile(tmp_path, monkeypatch, capsys)` |
| `tests/test_desktop_resources.py` | 174 | `path` |
| `tests/test_desktop_resources.py` | 175 | `profile` |
| `tests/test_desktop_resources.py` | 180 | `actual_host` |
| `tests/test_desktop_resources.py` | 181 | `observed` |
| `tests/test_desktop_resources.py` | 183 | `remember()` |
| `tests/test_desktop_resources.py` | 184 | `host` |
| `tests/test_desktop_resources.py` | 188 | `Interrupted(class)` |
| `tests/test_desktop_resources.py` | 189 | `__iter__(self)` |
| `tests/test_desktop_resources.py` | 200 | `reopened` |
| `tests/test_engine.py` | 17 | `test_unpublished_policy_comparison_uses_independent_oracle_and_retains_removed_checks()` |
| `tests/test_engine.py` | 19 | `active` |
| `tests/test_engine.py` | 19 | `operation` |
| `tests/test_engine.py` | 20 | `original` |
| `tests/test_engine.py` | 21 | `draft` |
| `tests/test_engine.py` | 23 | `rule` |
| `tests/test_engine.py` | 24 | `draft` |
| `tests/test_engine.py` | 25 | `result` |
| `tests/test_engine.py` | 29 | `row` |
| `tests/test_engine.py` | 29 | `rows` |
| `tests/test_engine.py` | 38 | `same` |
| `tests/test_engine.py` | 40 | `row` |
| `tests/test_engine.py` | 44 | `oracle(policy, operation)` |
| `tests/test_engine.py` | 46 | `results` |
| `tests/test_engine.py` | 48 | `quality(key, age)` |
| `tests/test_engine.py` | 50 | `e` |
| `tests/test_engine.py` | 50 | `records` |
| `tests/test_engine.py` | 53 | `e` |
| `tests/test_engine.py` | 55 | `e` |
| `tests/test_engine.py` | 57 | `e` |
| `tests/test_engine.py` | 59 | `e` |
| `tests/test_engine.py` | 61 | `e` |
| `tests/test_engine.py` | 63 | `e` |
| `tests/test_engine.py` | 67 | `value(key)` |
| `tests/test_engine.py` | 69 | `e` |
| `tests/test_engine.py` | 71 | `rule` |
| `tests/test_engine.py` | 72 | `reason` |
| `tests/test_engine.py` | 72 | `status` |
| `tests/test_engine.py` | 79 | `reason` |
| `tests/test_engine.py` | 81 | `reason` |
| `tests/test_engine.py` | 81 | `status` |
| `tests/test_engine.py` | 83 | `reason` |
| `tests/test_engine.py` | 85 | `status` |
| `tests/test_engine.py` | 87 | `actual` |
| `tests/test_engine.py` | 88 | `met` |
| `tests/test_engine.py` | 95 | `reason` |
| `tests/test_engine.py` | 95 | `status` |
| `tests/test_engine.py` | 101 | `r` |
| `tests/test_engine.py` | 101 | `statuses` |
| `tests/test_engine.py` | 102 | `overall` |
| `tests/test_engine.py` | 112 | `change(fact)` |
| `tests/test_engine.py` | 114 | `data` |
| `tests/test_engine.py` | 115 | `e` |
| `tests/test_engine.py` | 130 | `test_examples_real_opa(kind, status)` |
| `tests/test_engine.py` | 132 | `policy` |
| `tests/test_engine.py` | 133 | `operation` |
| `tests/test_engine.py` | 134 | `result` |
| `tests/test_engine.py` | 135 | `k` |
| `tests/test_engine.py` | 151 | `test_evidence_precedence(changes, reason, status)` |
| `tests/test_engine.py` | 153 | `result` |
| `tests/test_engine.py` | 154 | `r` |
| `tests/test_engine.py` | 154 | `row` |
| `tests/test_engine.py` | 158 | `test_conditional_unknown_and_false()` |
| `tests/test_engine.py` | 160 | `expected` |
| `tests/test_engine.py` | 160 | `value` |
| `tests/test_engine.py` | 161 | `result` |
| `tests/test_engine.py` | 162 | `r` |
| `tests/test_engine.py` | 175 | `test_context_and_policy_expiry(field, value)` |
| `tests/test_engine.py` | 177 | `data` |
| `tests/test_engine.py` | 179 | `result` |
| `tests/test_engine.py` | 181 | `row` |
| `tests/test_engine.py` | 184 | `test_conflicting_claims_and_permutation()` |
| `tests/test_engine.py` | 186 | `data` |
| `tests/test_engine.py` | 187 | `extra` |
| `tests/test_engine.py` | 190 | `a` |
| `tests/test_engine.py` | 192 | `b` |
| `tests/test_engine.py` | 196 | `test_seeded_oracle_and_numeric_operators()` |
| `tests/test_engine.py` | 198 | `rng` |
| `tests/test_engine.py` | 199 | `_` |
| `tests/test_engine.py` | 200 | `policy` |
| `tests/test_engine.py` | 201 | `operation` |
| `tests/test_engine.py` | 202 | `rule` |
| `tests/test_engine.py` | 205 | `record` |
| `tests/test_engine.py` | 213 | `p` |
| `tests/test_engine.py` | 214 | `o` |
| `tests/test_engine.py` | 215 | `result` |
| `tests/test_engine.py` | 216 | `k` |
| `tests/test_engine.py` | 229 | `test_invalid_evidence(changes)` |
| `tests/test_engine.py` | 251 | `test_invalid_policy(mutation)` |
| `tests/test_engine.py` | 253 | `data` |
| `tests/test_engine.py` | 259 | `test_policy_contradictions()` |
| `tests/test_engine.py` | 261 | `changes` |
| `tests/test_engine.py` | 261 | `index` |
| `tests/test_engine.py` | 266 | `data` |
| `tests/test_engine.py` | 267 | `duplicate` |
| `tests/test_engine.py` | 272 | `data` |
| `tests/test_engine.py` | 273 | `a` |
| `tests/test_engine.py` | 274 | `b` |
| `tests/test_engine.py` | 281 | `test_invalid_numeric(value)` |
| `tests/test_engine.py` | 287 | `test_duplicate_and_bounds()` |
| `tests/test_engine.py` | 289 | `data` |
| `tests/test_engine.py` | 296 | `data` |
| `tests/test_engine.py` | 313 | `test_malformed_result(monkeypatch, output)` |
| `tests/test_engine.py` | 322 | `test_output_inventory_and_aggregate()` |
| `tests/test_engine.py` | 324 | `policy` |
| `tests/test_engine.py` | 325 | `valid` |
| `tests/test_engine.py` | 326 | `mutation` |
| `tests/test_engine.py` | 333 | `data` |
| `tests/test_engine.py` | 340 | `test_unavailable(monkeypatch, error)` |
| `tests/test_engine.py` | 343 | `fail()` |
| `tests/test_engine.py` | 352 | `test_busy_nonzero_oversize(monkeypatch)` |
| `tests/test_engine.py` | 362 | `code` |
| `tests/test_engine.py` | 362 | `output` |
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
| `tests/test_owner_window.py` | 11 | `database_snapshot(store)` |
| `tests/test_owner_window.py` | 13 | `database` |
| `tests/test_owner_window.py` | 18 | `window(tmp_path)` |
| `tests/test_owner_window.py` | 20 | `root` |
| `tests/test_owner_window.py` | 22 | `view` |
| `tests/test_owner_window.py` | 39 | `credentials(view, name, password, confirmation)` |
| `tests/test_owner_window.py` | 41 | `password` |
| `tests/test_owner_window.py` | 47 | `test_actual_buttons_first_account_staff_and_no_password_retention(window, monkeypatch)` |
| `tests/test_owner_window.py` | 49 | `_` |
| `tests/test_owner_window.py` | 49 | `view` |
| `tests/test_owner_window.py` | 50 | `opened` |
| `tests/test_owner_window.py` | 69 | `original_host` |
| `tests/test_owner_window.py` | 84 | `test_folder_choice_and_unknown_existing_files_are_not_adopted(window, tmp_path, monkeypatch)` |
| `tests/test_owner_window.py` | 86 | `_` |
| `tests/test_owner_window.py` | 86 | `view` |
| `tests/test_owner_window.py` | 87 | `original` |
| `tests/test_owner_window.py` | 91 | `target` |
| `tests/test_owner_window.py` | 93 | `note` |
| `tests/test_owner_window.py` | 102 | `test_cancelled_or_busy_quit_retains_owner_until_actual_completion(window, monkeypatch)` |
| `tests/test_owner_window.py` | 104 | `root` |
| `tests/test_owner_window.py` | 104 | `view` |
| `tests/test_owner_window.py` | 113 | `busy()` |
| `tests/test_owner_window.py` | 116 | `change` |
| `tests/test_owner_window.py` | 126 | `test_identified_profile_automatically_reopens_without_reset(tmp_path, monkeypatch)` |
| `tests/test_owner_window.py` | 128 | `path` |
| `tests/test_owner_window.py` | 129 | `profile` |
| `tests/test_owner_window.py` | 133 | `before` |
| `tests/test_owner_window.py` | 135 | `opened` |
| `tests/test_owner_window.py` | 137 | `root` |
| `tests/test_owner_window.py` | 139 | `view` |
| `tests/test_owner_window.py` | 155 | `test_quit_after_real_startup_failure_releases_owner_and_retains_failure_exit(tmp_path, monkeypatch)` |
| `tests/test_owner_window.py` | 159 | `path` |
| `tests/test_owner_window.py` | 160 | `profile` |
| `tests/test_owner_window.py` | 165 | `actual_host` |
| `tests/test_owner_window.py` | 167 | `failed_host()` |
| `tests/test_owner_window.py` | 168 | `host` |
| `tests/test_owner_window.py` | 170 | `fail()` |
| `tests/test_owner_window.py` | 178 | `root` |
| `tests/test_owner_window.py` | 180 | `view` |
| `tests/test_owner_window.py` | 187 | `test_minimum_window_keeps_lifecycle_controls_visible_and_long_status_scrollable(window)` |
| `tests/test_owner_window.py` | 189 | `root` |
| `tests/test_owner_window.py` | 189 | `view` |
| `tests/test_owner_window.py` | 194 | `control` |
| `tests/test_owner_window.py` | 195 | `top` |
| `tests/test_portable_archive.py` | 17 | `APPLICATION` |
| `tests/test_portable_archive.py` | 21 | `test_roundtrip_keeps_one_application_root_and_metadata(tmp_path, suffix)` |
| `tests/test_portable_archive.py` | 23 | `bundle` |
| `tests/test_portable_archive.py` | 27 | `destination` |
| `tests/test_portable_archive.py` | 30 | `extracted` |
| `tests/test_portable_archive.py` | 38 | `test_posix_archive_keeps_relative_link_and_executable_mode(tmp_path)` |
| `tests/test_portable_archive.py` | 40 | `path` |
| `tests/test_portable_archive.py` | 41 | `output` |
| `tests/test_portable_archive.py` | 42 | `member` |
| `tests/test_portable_archive.py` | 45 | `link` |
| `tests/test_portable_archive.py` | 48 | `bundle` |
| `tests/test_portable_archive.py` | 68 | `test_member_escape_or_alias_is_rejected_before_writes(tmp_path, name)` |
| `tests/test_portable_archive.py` | 70 | `target` |
| `tests/test_portable_archive.py` | 71 | `output` |
| `tests/test_portable_archive.py` | 73 | `sentinel` |
| `tests/test_portable_archive.py` | 81 | `test_tar_link_escape_rejected_without_creating_links(tmp_path, target)` |
| `tests/test_portable_archive.py` | 83 | `path` |
| `tests/test_portable_archive.py` | 84 | `output` |
| `tests/test_portable_archive.py` | 85 | `member` |
| `tests/test_portable_archive.py` | 93 | `test_zip_symlink_and_duplicate_members_are_rejected(tmp_path)` |
| `tests/test_portable_archive.py` | 95 | `path` |
| `tests/test_portable_archive.py` | 96 | `output` |
| `tests/test_portable_archive.py` | 97 | `member` |
| `tests/test_portable_archive.py` | 102 | `path` |
| `tests/test_portable_archive.py` | 103 | `output` |
| `tests/test_portable_archive.py` | 104 | `_` |
| `tests/test_portable_archive.py` | 105 | `member` |
| `tests/test_portable_archive.py` | 111 | `test_member_content_and_metadata_budgets_are_checked(tmp_path, monkeypatch)` |
| `tests/test_portable_archive.py` | 113 | `path` |
| `tests/test_portable_archive.py` | 114 | `output` |
| `tests/test_portable_archive.py` | 120 | `path` |
| `tests/test_portable_archive.py` | 121 | `output` |
| `tests/test_profile_paths.py` | 12 | `files(directory)` |
| `tests/test_profile_paths.py` | 16 | `path` |
| `tests/test_profile_paths.py` | 21 | `junction_or_link(target, alias)` |
| `tests/test_profile_paths.py` | 34 | `test_actual_directory_alias_refused_before_target_or_parent_creation(tmp_path, ancestor)` |
| `tests/test_profile_paths.py` | 36 | `target` |
| `tests/test_profile_paths.py` | 38 | `alias` |
| `tests/test_profile_paths.py` | 40 | `chosen` |
| `tests/test_profile_paths.py` | 47 | `test_frozen_program_trees_refused_before_mkdir(tmp_path, monkeypatch, location)` |
| `tests/test_profile_paths.py` | 49 | `bundle` |
| `tests/test_profile_paths.py` | 50 | `executable` |
| `tests/test_profile_paths.py` | 51 | `internal` |
| `tests/test_profile_paths.py` | 58 | `parent` |
| `tests/test_profile_paths.py` | 63 | `chosen` |
| `tests/test_profile_paths.py` | 64 | `before` |
| `tests/test_profile_paths.py` | 68 | `outside` |
| `tests/test_profile_paths.py` | 83 | `test_real_hardlinked_member_refused_before_any_other_mutation(tmp_path, name)` |
| `tests/test_profile_paths.py` | 85 | `chosen` |
| `tests/test_profile_paths.py` | 86 | `profile` |
| `tests/test_profile_paths.py` | 88 | `destination` |
| `tests/test_profile_paths.py` | 89 | `target` |
| `tests/test_profile_paths.py` | 94 | `before` |
| `tests/test_profile_paths.py` | 100 | `test_bad_directory_kind_and_parent_traversal_are_not_created(tmp_path)` |
| `tests/test_profile_paths.py` | 102 | `ordinary` |
| `tests/test_profile_paths.py` | 111 | `test_read_only_missing_member_never_creates_it(tmp_path)` |
| `tests/test_profile_paths.py` | 113 | `path` |
| `tests/test_profile_paths.py` | 115 | `descriptor` |
| `tests/test_profile_paths.py` | 123 | `test_opened_identity_replacement_is_rejected_and_descriptor_closed(tmp_path, monkeypatch)` |
| `tests/test_profile_paths.py` | 125 | `path` |
| `tests/test_profile_paths.py` | 126 | `replacement` |
| `tests/test_profile_paths.py` | 129 | `original_open` |
| `tests/test_profile_paths.py` | 130 | `observed` |
| `tests/test_profile_paths.py` | 132 | `replace_then_open(candidate, flags, mode)` |
| `tests/test_profile_paths.py` | 134 | `descriptor` |
| `tests/test_profile_paths.py` | 140 | `descriptor` |
| `tests/test_profile_paths.py` | 150 | `test_existing_nonregular_identity_member_is_refused(tmp_path)` |
| `tests/test_profile_paths.py` | 152 | `chosen` |
| `tests/test_publication_text.py` | 15 | `edition(root, name, main, text)` |
| `tests/test_publication_text.py` | 17 | `path` |
| `tests/test_publication_text.py` | 19 | `package` |
| `tests/test_publication_text.py` | 34 | `test_named_office_xml_remains_visible(tmp_path, name, main)` |
| `tests/test_publication_text.py` | 36 | `text` |
| `tests/test_publication_text.py` | 40 | `test_unknown_binary_is_not_an_exclusion(tmp_path)` |
| `tests/test_publication_text.py` | 42 | `path` |
| `tests/test_publication_text.py` | 47 | `test_missing_document_root_is_rejected(tmp_path)` |
| `tests/test_publication_text.py` | 53 | `test_invalid_zip_is_rejected(tmp_path)` |
| `tests/test_publication_text.py` | 55 | `path` |
| `tests/test_publication_text.py` | 62 | `test_invalid_utf8_xml_is_rejected(tmp_path)` |
| `tests/test_publication_text.py` | 68 | `test_expansion_budget_is_active(tmp_path)` |
| `tests/test_publication_text.py` | 70 | `path` |
| `tests/test_publication_text.py` | 78 | `test_active_or_embedded_payloads_are_not_reviewed_text(tmp_path, member)` |
| `tests/test_publication_text.py` | 80 | `path` |
| `tests/test_publication_text.py` | 81 | `package` |
| `tests/test_publication_text.py` | 88 | `test_actual_repository_guard_reads_credentials_inside_word(tmp_path, monkeypatch, part)` |
| `tests/test_publication_text.py` | 97 | `path` |
| `tests/test_publication_text.py` | 98 | `token` |
| `tests/test_publication_text.py` | 100 | `package` |
| `tests/test_publication_text.py` | 112 | `spec` |
| `tests/test_publication_text.py` | 116 | `checker` |
| `tests/test_runtime_notices.py` | 13 | `test_all_thirteen_actual_notice_contracts_in_one_fresh_owned_interpreter()` |
| `tests/test_runtime_notices.py` | 15 | `root` |
| `tests/test_runtime_notices.py` | 16 | `cases` |
| `tests/test_runtime_notices.py` | 17 | `temporary` |
| `tests/test_runtime_notices.py` | 18 | `result_path` |
| `tests/test_runtime_notices.py` | 19 | `result` |
| `tests/test_runtime_notices.py` | 35 | `records` |
| `tests/test_runtime_notices.py` | 37 | `item` |
| `tests/test_runtime_notices.py` | 38 | `item` |
| `tests/test_runtime_notices.py` | 39 | `receipt` |
| `tests/test_runtime_notices.py` | 41 | `item` |
| `tests/test_runtime_notices.py` | 52 | `target` |
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
| `tools/check_repo.py` | 10 | `main()` |
| `tools/check_repo.py` | 12 | `path` |
| `tools/check_repo.py` | 13 | `relative` |
| `tools/check_repo.py` | 14 | `content` |
| `tools/check_repo.py` | 23 | `ref` |
| `tools/check_repo.py` | 28 | `builtin` |
| `tools/check_repo.py` | 30 | `budget` |
| `tools/check_repo.py` | 30 | `suffix` |
| `tools/check_repo.py` | 31 | `size` |
| `tools/check_repo.py` | 32 | `p` |
| `tools/docs_index.py` | 19 | `ROOT` |
| `tools/docs_index.py` | 20 | `EXCLUDE` |
| `tools/docs_index.py` | 34 | `SPECIAL` |
| `tools/docs_index.py` | 65 | `files()` |
| `tools/docs_index.py` | 67 | `result` |
| `tools/docs_index.py` | 68 | `children` |
| `tools/docs_index.py` | 68 | `directory` |
| `tools/docs_index.py` | 68 | `names` |
| `tools/docs_index.py` | 69 | `child` |
| `tools/docs_index.py` | 70 | `name` |
| `tools/docs_index.py` | 76 | `render()` |
| `tools/docs_index.py` | 78 | `catalog` |
| `tools/docs_index.py` | 86 | `source` |
| `tools/docs_index.py` | 95 | `path` |
| `tools/docs_index.py` | 96 | `relative` |
| `tools/docs_index.py` | 97 | `content` |
| `tools/docs_index.py` | 98 | `description` |
| `tools/docs_index.py` | 101 | `line` |
| `tools/docs_index.py` | 109 | `records` |
| `tools/docs_index.py` | 111 | `node` |
| `tools/docs_index.py` | 113 | `args` |
| `tools/docs_index.py` | 116 | `a` |
| `tools/docs_index.py` | 122 | `line` |
| `tools/docs_index.py` | 122 | `value` |
| `tools/docs_index.py` | 132 | `line` |
| `tools/docs_index.py` | 132 | `value` |
| `tools/docs_index.py` | 135 | `line` |
| `tools/docs_index.py` | 135 | `name` |
| `tools/docs_index.py` | 136 | `node` |
| `tools/docs_index.py` | 150 | `main()` |
| `tools/docs_index.py` | 152 | `content` |
| `tools/docs_index.py` | 152 | `relative` |
| `tools/docs_index.py` | 153 | `path` |
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
| `tools/package_app.py` | 29 | `ROOT` |
| `tools/package_app.py` | 30 | `APPLICATION` |
| `tools/package_app.py` | 31 | `PRODUCT` |
| `tools/package_app.py` | 34 | `restore_vendor_opa(bundle, source, expected)` |
| `tools/package_app.py` | 46 | `target` |
| `tools/package_app.py` | 54 | `stream` |
| `tools/package_app.py` | 55 | `original` |
| `tools/package_app.py` | 57 | `stream` |
| `tools/package_app.py` | 58 | `collected` |
| `tools/package_app.py` | 62 | `stream` |
| `tools/package_app.py` | 63 | `restored` |
| `tools/package_app.py` | 69 | `build_python_supported(version, releaselevel)` |
| `tools/package_app.py` | 79 | `configuration(root)` |
| `tools/package_app.py` | 81 | `project` |
| `tools/package_app.py` | 82 | `package` |
| `tools/package_app.py` | 83 | `lock` |
| `tools/package_app.py` | 84 | `version` |
| `tools/package_app.py` | 98 | `source_metadata(version)` |
| `tools/package_app.py` | 104 | `command` |
| `tools/package_app.py` | 105 | `source` |
| `tools/package_app.py` | 106 | `changed` |
| `tools/package_app.py` | 128 | `main(argv)` |
| `tools/package_app.py` | 130 | `parser` |
| `tools/package_app.py` | 137 | `args` |
| `tools/package_app.py` | 147 | `opa` |
| `tools/package_app.py` | 163 | `version` |
| `tools/package_app.py` | 164 | `notices` |
| `tools/package_app.py` | 164 | `versions` |
| `tools/package_app.py` | 165 | `metadata` |
| `tools/package_app.py` | 167 | `generated` |
| `tools/package_app.py` | 169 | `identity_file` |
| `tools/package_app.py` | 171 | `notice_file` |
| `tools/package_app.py` | 173 | `pyinstaller` |
| `tools/package_app.py` | 174 | `licenses` |
| `tools/package_app.py` | 176 | `path` |
| `tools/package_app.py` | 180 | `build` |
| `tools/package_app.py` | 181 | `command` |
| `tools/package_app.py` | 198 | `destination` |
| `tools/package_app.py` | 198 | `source` |
| `tools/package_app.py` | 210 | `source_path` |
| `tools/package_app.py` | 212 | `source_path` |
| `tools/package_app.py` | 213 | `command` |
| `tools/package_app.py` | 214 | `hidden` |
| `tools/package_app.py` | 219 | `command` |
| `tools/package_app.py` | 220 | `command` |
| `tools/package_app.py` | 221 | `environment` |
| `tools/package_app.py` | 227 | `bundle` |
| `tools/package_app.py` | 228 | `vendor_identity` |
| `tools/package_app.py` | 233 | `suffix` |
| `tools/package_app.py` | 234 | `name` |
| `tools/package_app.py` | 235 | `output` |
| `tools/package_app.py` | 241 | `archive` |
| `tools/package_app.py` | 241 | `sidecar` |
| `tools/package_app.py` | 245 | `temporary` |
| `tools/package_app.py` | 246 | `extracted` |
| `tools/package_app.py` | 247 | `executable` |
| `tools/package_app.py` | 260 | `stream` |
| `tools/package_app.py` | 261 | `digest` |
| `tools/portable_archive.py` | 17 | `MAX_BYTES` |
| `tools/portable_archive.py` | 18 | `MAX_MEMBERS` |
| `tools/portable_archive.py` | 21 | `require(condition, message)` |
| `tools/portable_archive.py` | 27 | `safe_name(name, application)` |
| `tools/portable_archive.py` | 29 | `parts` |
| `tools/portable_archive.py` | 30 | `raw_parts` |
| `tools/portable_archive.py` | 38 | `part` |
| `tools/portable_archive.py` | 39 | `char` |
| `tools/portable_archive.py` | 44 | `safe_link(name, target, application)` |
| `tools/portable_archive.py` | 51 | `char` |
| `tools/portable_archive.py` | 54 | `resolved` |
| `tools/portable_archive.py` | 60 | `create_archive(bundle, archive)` |
| `tools/portable_archive.py` | 66 | `members` |
| `tools/portable_archive.py` | 68 | `total` |
| `tools/portable_archive.py` | 69 | `path` |
| `tools/portable_archive.py` | 78 | `total` |
| `tools/portable_archive.py` | 82 | `path` |
| `tools/portable_archive.py` | 84 | `target` |
| `tools/portable_archive.py` | 85 | `path` |
| `tools/portable_archive.py` | 88 | `target` |
| `tools/portable_archive.py` | 89 | `path` |
| `tools/portable_archive.py` | 97 | `inspected(archive, application)` |
| `tools/portable_archive.py` | 102 | `members` |
| `tools/portable_archive.py` | 103 | `total` |
| `tools/portable_archive.py` | 104 | `names` |
| `tools/portable_archive.py` | 106 | `source` |
| `tools/portable_archive.py` | 107 | `member` |
| `tools/portable_archive.py` | 111 | `total` |
| `tools/portable_archive.py` | 112 | `kind` |
| `tools/portable_archive.py` | 114 | `source` |
| `tools/portable_archive.py` | 115 | `member` |
| `tools/portable_archive.py` | 124 | `total` |
| `tools/portable_archive.py` | 129 | `kind` |
| `tools/portable_archive.py` | 136 | `member` |
| `tools/portable_archive.py` | 137 | `name` |
| `tools/portable_archive.py` | 143 | `archive_metadata(archive, application)` |
| `tools/portable_archive.py` | 145 | `kind` |
| `tools/portable_archive.py` | 145 | `members` |
| `tools/portable_archive.py` | 146 | `expected` |
| `tools/portable_archive.py` | 147 | `m` |
| `tools/portable_archive.py` | 147 | `selected` |
| `tools/portable_archive.py` | 149 | `member` |
| `tools/portable_archive.py` | 150 | `size` |
| `tools/portable_archive.py` | 155 | `source` |
| `tools/portable_archive.py` | 156 | `value` |
| `tools/portable_archive.py` | 158 | `source` |
| `tools/portable_archive.py` | 159 | `stream` |
| `tools/portable_archive.py` | 161 | `value` |
| `tools/portable_archive.py` | 166 | `extract_archive(archive, destination, application)` |
| `tools/portable_archive.py` | 168 | `kind` |
| `tools/portable_archive.py` | 168 | `members` |
| `tools/portable_archive.py` | 171 | `source` |
| `tools/portable_archive.py` | 172 | `member` |
| `tools/portable_archive.py` | 173 | `target` |
| `tools/portable_archive.py` | 178 | `total` |
| `tools/portable_archive.py` | 179 | `incoming` |
| `tools/portable_archive.py` | 179 | `outgoing` |
| `tools/portable_archive.py` | 180 | `chunk` |
| `tools/portable_archive.py` | 181 | `total` |
| `tools/portable_archive.py` | 186 | `source` |
| `tools/portable_archive.py` | 188 | `bundle` |
| `tools/portable_archive.py` | 190 | `path` |
| `tools/profile_admission_smoke.py` | 10 | `snapshot(root)` |
| `tools/profile_admission_smoke.py` | 14 | `path` |
| `tools/profile_admission_smoke.py` | 19 | `verify(executable, output, environment)` |
| `tools/profile_admission_smoke.py` | 21 | `fixture` |
| `tools/profile_admission_smoke.py` | 23 | `before_program` |
| `tools/profile_admission_smoke.py` | 24 | `selections` |
| `tools/profile_admission_smoke.py` | 28 | `label` |
| `tools/profile_admission_smoke.py` | 29 | `folder` |
| `tools/profile_admission_smoke.py` | 31 | `target` |
| `tools/profile_admission_smoke.py` | 33 | `alias` |
| `tools/profile_admission_smoke.py` | 43 | `results` |
| `tools/profile_admission_smoke.py` | 44 | `label` |
| `tools/profile_admission_smoke.py` | 44 | `selected` |
| `tools/profile_admission_smoke.py` | 45 | `result` |
| `tools/profile_admission_smoke.py` | 64 | `label` |
| `tools/publication_text.py` | 11 | `EDITION_ROOTS` |
| `tools/publication_text.py` | 17 | `MAX_PACKAGE_BYTES` |
| `tools/publication_text.py` | 18 | `MAX_EXPANDED_BYTES` |
| `tools/publication_text.py` | 19 | `MAX_MEMBER_BYTES` |
| `tools/publication_text.py` | 20 | `MAX_MEMBERS` |
| `tools/publication_text.py` | 23 | `public_text(path, root)` |
| `tools/publication_text.py` | 25 | `relative` |
| `tools/publication_text.py` | 29 | `source` |
| `tools/publication_text.py` | 32 | `package` |
| `tools/publication_text.py` | 33 | `members` |
| `tools/publication_text.py` | 34 | `member` |
| `tools/publication_text.py` | 34 | `names` |
| `tools/publication_text.py` | 39 | `member` |
| `tools/publication_text.py` | 41 | `result` |
| `tools/publication_text.py` | 42 | `member` |
| `tools/publication_text.py` | 52 | `stream` |
| `tools/publication_text.py` | 53 | `payload` |
| `tools/runtime_notices.py` | 10 | `UPSTREAM_904` |
| `tools/runtime_notices.py` | 22 | `read_tcl_notice(interpreter, path)` |
| `tools/runtime_notices.py` | 27 | `channel` |
| `tools/runtime_notices.py` | 29 | `code` |
| `tools/runtime_notices.py` | 34 | `raw` |
| `tools/runtime_notices.py` | 37 | `raw` |
| `tools/runtime_notices.py` | 43 | `gui_notice(interpreter, root, kind, version, library, system)` |
| `tools/runtime_notices.py` | 45 | `system` |
| `tools/runtime_notices.py` | 58 | `path` |
| `tools/runtime_notices.py` | 60 | `framework` |
| `tools/runtime_notices.py` | 63 | `commit` |
| `tools/runtime_notices.py` | 63 | `expected` |
| `tools/runtime_notices.py` | 64 | `stream` |
| `tools/runtime_notices.py` | 65 | `raw` |
| `tools/runtime_notices.py` | 81 | `stream` |
| `tools/runtime_notices.py` | 82 | `raw` |
| `tools/runtime_notices.py` | 96 | `collect(root)` |
| `tools/runtime_notices.py` | 100 | `window` |
| `tools/runtime_notices.py` | 103 | `versions` |
| `tools/runtime_notices.py` | 107 | `value` |
| `tools/runtime_notices.py` | 109 | `blocks` |
| `tools/runtime_notices.py` | 110 | `kind` |
| `tools/runtime_notices.py` | 110 | `library` |
| `tools/runtime_notices.py` | 110 | `version` |
| `tools/runtime_notices.py` | 114 | `provenance` |
| `tools/runtime_notices.py` | 114 | `raw` |
| `tools/runtime_notices.py` | 120 | `names` |
| `tools/runtime_notices.py` | 123 | `name` |
| `tools/runtime_notices.py` | 124 | `info` |
| `tools/runtime_notices.py` | 125 | `files` |
| `tools/runtime_notices.py` | 127 | `path` |
| `tools/runtime_notices.py` | 133 | `path` |
| `tools/runtime_notices.py` | 134 | `stream` |
| `tools/runtime_notices.py` | 135 | `raw` |
| `tools/runtime_notices.py` | 139 | `raw` |
| `tools/runtime_notices.py` | 139 | `title` |
| `tools/smoke_app.py` | 22 | `ROOT` |
| `tools/smoke_app.py` | 26 | `require(condition, message)` |
| `tools/smoke_app.py` | 32 | `request(url, path)` |
| `tools/smoke_app.py` | 34 | `target` |
| `tools/smoke_app.py` | 43 | `connection` |
| `tools/smoke_app.py` | 46 | `response` |
| `tools/smoke_app.py` | 47 | `raw` |
| `tools/smoke_app.py` | 57 | `main(argv)` |
| `tools/smoke_app.py` | 62 | `parser` |
| `tools/smoke_app.py` | 65 | `args` |
| `tools/smoke_app.py` | 66 | `executable` |
| `tools/smoke_app.py` | 67 | `expected` |
| `tools/smoke_app.py` | 75 | `output` |
| `tools/smoke_app.py` | 77 | `node` |
| `tools/smoke_app.py` | 79 | `profile_directory` |
| `tools/smoke_app.py` | 80 | `password` |
| `tools/smoke_app.py` | 81 | `profile` |
| `tools/smoke_app.py` | 82 | `expected_cookie` |
| `tools/smoke_app.py` | 84 | `role` |
| `tools/smoke_app.py` | 88 | `allowed` |
| `tools/smoke_app.py` | 104 | `environment` |
| `tools/smoke_app.py` | 104 | `key` |
| `tools/smoke_app.py` | 104 | `value` |
| `tools/smoke_app.py` | 113 | `diagnostic` |
| `tools/smoke_app.py` | 122 | `lines` |
| `tools/smoke_app.py` | 123 | `line` |
| `tools/smoke_app.py` | 126 | `actual_runtime` |
| `tools/smoke_app.py` | 129 | `key` |
| `tools/smoke_app.py` | 136 | `process` |
| `tools/smoke_app.py` | 146 | `events` |
| `tools/smoke_app.py` | 147 | `log` |
| `tools/smoke_app.py` | 149 | `read_output()` |
| `tools/smoke_app.py` | 152 | `line` |
| `tools/smoke_app.py` | 158 | `reader` |
| `tools/smoke_app.py` | 160 | `actual_exit` |
| `tools/smoke_app.py` | 160 | `forced` |
| `tools/smoke_app.py` | 160 | `passed` |
| `tools/smoke_app.py` | 160 | `url` |
| `tools/smoke_app.py` | 162 | `deadline` |
| `tools/smoke_app.py` | 164 | `remaining` |
| `tools/smoke_app.py` | 166 | `line` |
| `tools/smoke_app.py` | 169 | `ready` |
| `tools/smoke_app.py` | 176 | `url` |
| `tools/smoke_app.py` | 177 | `code` |
| `tools/smoke_app.py` | 177 | `raw` |
| `tools/smoke_app.py` | 223 | `actual_exit` |
| `tools/smoke_app.py` | 229 | `target` |
| `tools/smoke_app.py` | 231 | `connection` |
| `tools/smoke_app.py` | 237 | `reopened` |
| `tools/smoke_app.py` | 246 | `line` |
| `tools/smoke_app.py` | 248 | `passed` |
| `tools/smoke_app.py` | 256 | `forced` |
| `workbench/__init__.py` | 3 | `__version__` |
| `workbench/__main__.py` | 15 | `main()` |
| `workbench/__main__.py` | 17 | `parser` |
| `workbench/__main__.py` | 19 | `commands` |
| `workbench/__main__.py` | 21 | `user` |
| `workbench/__main__.py` | 24 | `serve` |
| `workbench/__main__.py` | 26 | `args` |
| `workbench/__main__.py` | 27 | `store` |
| `workbench/__main__.py` | 32 | `password` |
| `workbench/api.py` | 20 | `HEADERS` |
| `workbench/api.py` | 30 | `create_app(database, port)` |
| `workbench/api.py` | 36 | `origin` |
| `workbench/api.py` | 37 | `authority` |
| `workbench/api.py` | 38 | `app` |
| `workbench/api.py` | 45 | `boundary(request, call_next)` |
| `workbench/api.py` | 47 | `response` |
| `workbench/api.py` | 49 | `response` |
| `workbench/api.py` | 51 | `response` |
| `workbench/api.py` | 57 | `response` |
| `workbench/api.py` | 59 | `response` |
| `workbench/api.py` | 61 | `chunks` |
| `workbench/api.py` | 62 | `size` |
| `workbench/api.py` | 65 | `chunk` |
| `workbench/api.py` | 66 | `size` |
| `workbench/api.py` | 68 | `response` |
| `workbench/api.py` | 76 | `response` |
| `workbench/api.py` | 78 | `response` |
| `workbench/api.py` | 83 | `invalid(_request, error)` |
| `workbench/api.py` | 88 | `e` |
| `workbench/api.py` | 94 | `health()` |
| `workbench/api.py` | 107 | `login(body, request)` |
| `workbench/api.py` | 109 | `token` |
| `workbench/api.py` | 109 | `user` |
| `workbench/api.py` | 110 | `response` |
| `workbench/api.py` | 115 | `me(request)` |
| `workbench/api.py` | 120 | `logout(request)` |
| `workbench/api.py` | 123 | `response` |
| `workbench/api.py` | 128 | `workspace(request)` |
| `workbench/api.py` | 130 | `user` |
| `workbench/api.py` | 131 | `policy` |
| `workbench/api.py` | 131 | `version` |
| `workbench/api.py` | 132 | `audit` |
| `workbench/api.py` | 132 | `history` |
| `workbench/api.py` | 141 | `templates(request)` |
| `workbench/api.py` | 147 | `publish(body, request)` |
| `workbench/api.py` | 149 | `user` |
| `workbench/api.py` | 155 | `assess(body, request)` |
| `workbench/api.py` | 157 | `user` |
| `workbench/api.py` | 158 | `policy` |
| `workbench/api.py` | 158 | `version` |
| `workbench/api.py` | 162 | `result` |
| `workbench/api.py` | 165 | `identifier` |
| `workbench/api.py` | 169 | `preview(body, request)` |
| `workbench/api.py` | 172 | `policy` |
| `workbench/api.py` | 172 | `version` |
| `workbench/api.py` | 176 | `result` |
| `workbench/api.py` | 184 | `report(identifier, request)` |
| `workbench/api.py` | 189 | `review(identifier, body, request)` |
| `workbench/api.py` | 191 | `user` |
| `workbench/api.py` | 196 | `index()` |
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
| `workbench/auth.py` | 80 | `session_cookie_name(request)` |
| `workbench/auth.py` | 85 | `identity(request)` |
| `workbench/auth.py` | 87 | `token` |
| `workbench/auth.py` | 90 | `db` |
| `workbench/auth.py` | 91 | `row` |
| `workbench/auth.py` | 100 | `authorize(request, role)` |
| `workbench/auth.py` | 102 | `user` |
| `workbench/auth.py` | 112 | `sign_out(request)` |
| `workbench/auth.py` | 115 | `db` |
| `workbench/desktop.py` | 21 | `ROOT` |
| `workbench/desktop.py` | 24 | `read_resource(path)` |
| `workbench/desktop.py` | 26 | `descriptor` |
| `workbench/desktop.py` | 29 | `stream` |
| `workbench/desktop.py` | 30 | `info` |
| `workbench/desktop.py` | 33 | `raw` |
| `workbench/desktop.py` | 39 | `identity(root)` |
| `workbench/desktop.py` | 42 | `value` |
| `workbench/desktop.py` | 61 | `console_session(directory, metadata)` |
| `workbench/desktop.py` | 63 | `profile` |
| `workbench/desktop.py` | 64 | `host` |
| `workbench/desktop.py` | 68 | `host` |
| `workbench/desktop.py` | 75 | `line` |
| `workbench/desktop.py` | 90 | `main(argv)` |
| `workbench/desktop.py` | 92 | `parser` |
| `workbench/desktop.py` | 109 | `args` |
| `workbench/desktop.py` | 113 | `metadata` |
| `workbench/desktop.py` | 118 | `root` |
| `workbench/desktop.py` | 121 | `versions` |
| `workbench/desktop.py` | 126 | `directory` |
| `workbench/desktop.py` | 134 | `root` |
| `workbench/desktop.py` | 135 | `window` |
| `workbench/desktop_host.py` | 18 | `OwnedServer(class)` |
| `workbench/desktop_host.py` | 21 | `__init__(self, config, ready, record)` |
| `workbench/desktop_host.py` | 27 | `startup(self, sockets)` |
| `workbench/desktop_host.py` | 36 | `Host(class)` |
| `workbench/desktop_host.py` | 39 | `__init__(self, profile, metadata)` |
| `workbench/desktop_host.py` | 54 | `app` |
| `workbench/desktop_host.py` | 56 | `config` |
| `workbench/desktop_host.py` | 76 | `_run(self)` |
| `workbench/desktop_host.py` | 89 | `start(self, timeout)` |
| `workbench/desktop_host.py` | 97 | `stop(self, timeout)` |
| `workbench/desktop_profile.py` | 19 | `PRODUCT` |
| `workbench/desktop_profile.py` | 20 | `ROLES` |
| `workbench/desktop_profile.py` | 21 | `FIRST_ROLE` |
| `workbench/desktop_profile.py` | 24 | `default_directory()` |
| `workbench/desktop_profile.py` | 27 | `base` |
| `workbench/desktop_profile.py` | 29 | `base` |
| `workbench/desktop_profile.py` | 31 | `base` |
| `workbench/desktop_profile.py` | 37 | `read_marker(path)` |
| `workbench/desktop_profile.py` | 39 | `descriptor` |
| `workbench/desktop_profile.py` | 40 | `stream` |
| `workbench/desktop_profile.py` | 41 | `info` |
| `workbench/desktop_profile.py` | 44 | `raw` |
| `workbench/desktop_profile.py` | 47 | `value` |
| `workbench/desktop_profile.py` | 59 | `Profile(class)` |
| `workbench/desktop_profile.py` | 62 | `__init__(self, directory)` |
| `workbench/desktop_profile.py` | 64 | `directory` |
| `workbench/desktop_profile.py` | 68 | `marker` |
| `workbench/desktop_profile.py` | 74 | `stream` |
| `workbench/desktop_profile.py` | 78 | `namespace` |
| `workbench/desktop_profile.py` | 80 | `lock` |
| `workbench/desktop_profile.py` | 96 | `database` |
| `workbench/desktop_profile.py` | 105 | `count_users(self)` |
| `workbench/desktop_profile.py` | 107 | `database` |
| `workbench/desktop_profile.py` | 110 | `create_account(self, username, password, confirmation, role)` |
| `workbench/desktop_profile.py` | 120 | `close(self)` |
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
| `workbench/impact.py` | 8 | `policy_impact(active, draft, operation)` |
| `workbench/impact.py` | 10 | `after` |
| `workbench/impact.py` | 10 | `before` |
| `workbench/impact.py` | 11 | `old_rules` |
| `workbench/impact.py` | 11 | `rule` |
| `workbench/impact.py` | 12 | `new_rules` |
| `workbench/impact.py` | 12 | `rule` |
| `workbench/impact.py` | 13 | `old` |
| `workbench/impact.py` | 13 | `row` |
| `workbench/impact.py` | 14 | `new` |
| `workbench/impact.py` | 14 | `row` |
| `workbench/impact.py` | 15 | `checks` |
| `workbench/impact.py` | 16 | `identifier` |
| `workbench/impact.py` | 26 | `inputs` |
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
| `workbench/models.py` | 192 | `Preview(class)` |
| `workbench/models.py` | 195 | `operation` |
| `workbench/models.py` | 198 | `Review(class)` |
| `workbench/models.py` | 201 | `decision` |
| `workbench/models.py` | 202 | `note` |
| `workbench/owner_window.py` | 19 | `OwnerWindow(class)` |
| `workbench/owner_window.py` | 22 | `__init__(self, root, directory, metadata)` |
| `workbench/owner_window.py` | 41 | `shell` |
| `workbench/owner_window.py` | 44 | `actions` |
| `workbench/owner_window.py` | 52 | `content` |
| `workbench/owner_window.py` | 55 | `scrollbar` |
| `workbench/owner_window.py` | 59 | `body` |
| `workbench/owner_window.py` | 60 | `item` |
| `workbench/owner_window.py` | 81 | `location` |
| `workbench/owner_window.py` | 93 | `account` |
| `workbench/owner_window.py` | 103 | `caption` |
| `workbench/owner_window.py` | 103 | `index` |
| `workbench/owner_window.py` | 103 | `secret` |
| `workbench/owner_window.py` | 103 | `variable` |
| `workbench/owner_window.py` | 112 | `entry` |
| `workbench/owner_window.py` | 135 | `choose_directory(self)` |
| `workbench/owner_window.py` | 137 | `selected` |
| `workbench/owner_window.py` | 143 | `open_profile(self)` |
| `workbench/owner_window.py` | 149 | `control` |
| `workbench/owner_window.py` | 166 | `create_account(self)` |
| `workbench/owner_window.py` | 188 | `start_host(self)` |
| `workbench/owner_window.py` | 200 | `open_browser(self)` |
| `workbench/owner_window.py` | 205 | `quit(self)` |
| `workbench/owner_window.py` | 215 | `stop(self)` |
| `workbench/profile_paths.py` | 13 | `alias(info)` |
| `workbench/profile_paths.py` | 20 | `member(path)` |
| `workbench/profile_paths.py` | 23 | `info` |
| `workbench/profile_paths.py` | 26 | `expected` |
| `workbench/profile_paths.py` | 32 | `admitted_directory(path)` |
| `workbench/profile_paths.py` | 34 | `path` |
| `workbench/profile_paths.py` | 37 | `ancestor` |
| `workbench/profile_paths.py` | 40 | `executable_root` |
| `workbench/profile_paths.py` | 41 | `roots` |
| `workbench/profile_paths.py` | 42 | `parent` |
| `workbench/profile_paths.py` | 43 | `root` |
| `workbench/profile_paths.py` | 48 | `workspace_members(directory)` |
| `workbench/profile_paths.py` | 50 | `name` |
| `workbench/profile_paths.py` | 63 | `open_member(path, flags)` |
| `workbench/profile_paths.py` | 65 | `prior` |
| `workbench/profile_paths.py` | 66 | `flags` |
| `workbench/profile_paths.py` | 72 | `flags` |
| `workbench/profile_paths.py` | 73 | `descriptor` |
| `workbench/profile_paths.py` | 75 | `opened` |
| `workbench/runtime_gui.py` | 7 | `inspect_tk(root, metadata)` |
| `workbench/runtime_gui.py` | 9 | `versions` |
| `workbench/runtime_gui.py` | 13 | `value` |
| `workbench/runtime_gui.py` | 16 | `name` |
| `workbench/runtime_gui.py` | 16 | `value` |
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
| `ui/src/env.d.ts` | 2 | `__APP_VERSION__` |
| `ui/src/import_file.test.ts` | 11 | `value` |
| `ui/src/import_file.test.ts` | 23 | `text` |
| `ui/src/import_file.test.ts` | 34 | `incorrectMetadata` |
| `ui/src/import_file.ts` | 2 | `MAX_IMPORT_BYTES` |
| `ui/src/import_file.ts` | 5 | `objectFromText` |
| `ui/src/import_file.ts` | 5 | `text` |
| `ui/src/import_file.ts` | 8 | `value` |
| `ui/src/import_file.ts` | 11 | `stack` |
| `ui/src/import_file.ts` | 12 | `visited` |
| `ui/src/import_file.ts` | 15 | `[node, depth]` |
| `ui/src/import_file.ts` | 21 | `child` |
| `ui/src/import_file.ts` | 27 | `readObjectFile` |
| `ui/src/import_file.ts` | 28 | `file` |
| `ui/src/import_file.ts` | 32 | `bytes` |
| `ui/src/main.ts` | 13 | `Rule` |
| `ui/src/main.ts` | 23 | `Policy` |
| `ui/src/main.ts` | 27 | `Workspace` |
| `ui/src/main.ts` | 33 | `root` |
| `ui/src/main.ts` | 48 | `el` |
| `ui/src/main.ts` | 48 | `id` |
| `ui/src/main.ts` | 52 | `text` |
| `ui/src/main.ts` | 52 | `tag` |
| `ui/src/main.ts` | 52 | `value` |
| `ui/src/main.ts` | 53 | `node` |
| `ui/src/main.ts` | 57 | `user` |
| `ui/src/main.ts` | 58 | `workspace` |
| `ui/src/main.ts` | 59 | `report` |
| `ui/src/main.ts` | 60 | `templates` |
| `ui/src/main.ts` | 61 | `revision` |
| `ui/src/main.ts` | 62 | `importEpoch` |
| `ui/src/main.ts` | 63 | `policyDraftVersion` |
| `ui/src/main.ts` | 64 | `busy` |
| `ui/src/main.ts` | 65 | `Impact` |
| `ui/src/main.ts` | 78 | `impact` |
| `ui/src/main.ts` | 79 | `previewButton` |
| `ui/src/main.ts` | 83 | `impactDownload` |
| `ui/src/main.ts` | 88 | `impactOutput` |
| `ui/src/main.ts` | 95 | `clearImpact` |
| `ui/src/main.ts` | 105 | `requested` |
| `ui/src/main.ts` | 106 | `result` |
| `ui/src/main.ts` | 125 | `list` |
| `ui/src/main.ts` | 126 | `check` |
| `ui/src/main.ts` | 140 | `url` |
| `ui/src/main.ts` | 143 | `anchor` |
| `ui/src/main.ts` | 150 | `api` |
| `ui/src/main.ts` | 150 | `path` |
| `ui/src/main.ts` | 150 | `body` |
| `ui/src/main.ts` | 151 | `response` |
| `ui/src/main.ts` | 163 | `result` |
| `ui/src/main.ts` | 168 | `invalidate` |
| `ui/src/main.ts` | 185 | `action` |
| `ui/src/main.ts` | 185 | `task` |
| `ui/src/main.ts` | 194 | `id` |
| `ui/src/main.ts` | 198 | `error` |
| `ui/src/main.ts` | 207 | `permissions` |
| `ui/src/main.ts` | 229 | `refresh` |
| `ui/src/main.ts` | 229 | `preserveDraft` |
| `ui/src/main.ts` | 250 | `item` |
| `ui/src/main.ts` | 251 | `node` |
| `ui/src/main.ts` | 252 | `button` |
| `ui/src/main.ts` | 271 | `item` |
| `ui/src/main.ts` | 284 | `renderReport` |
| `ui/src/main.ts` | 286 | `result` |
| `ui/src/main.ts` | 287 | `summary` |
| `ui/src/main.ts` | 300 | `policy` |
| `ui/src/main.ts` | 301 | `check` |
| `ui/src/main.ts` | 302 | `rule` |
| `ui/src/main.ts` | 302 | `r` |
| `ui/src/main.ts` | 303 | `row` |
| `ui/src/main.ts` | 309 | `source` |
| `ui/src/main.ts` | 310 | `link` |
| `ui/src/main.ts` | 320 | `loadReport` |
| `ui/src/main.ts` | 321 | `identifier` |
| `ui/src/main.ts` | 322 | `requested` |
| `ui/src/main.ts` | 324 | `selected` |
| `ui/src/main.ts` | 335 | `signedIn` |
| `ui/src/main.ts` | 350 | `event` |
| `ui/src/main.ts` | 374 | `node` |
| `ui/src/main.ts` | 385 | `requested` |
| `ui/src/main.ts` | 386 | `operation` |
| `ui/src/main.ts` | 387 | `result` |
| `ui/src/main.ts` | 407 | `requested` |
| `ui/src/main.ts` | 408 | `published` |
| `ui/src/main.ts` | 430 | `[id, decision]` |
| `ui/src/main.ts` | 435 | `note` |
| `ui/src/main.ts` | 442 | `identifier` |
| `ui/src/main.ts` | 443 | `requested` |
| `ui/src/main.ts` | 448 | `loaded` |
| `ui/src/main.ts` | 475 | `url` |
| `ui/src/main.ts` | 478 | `link` |
| `ui/src/main.ts` | 486 | `importDraft` |
| `ui/src/main.ts` | 487 | `kind` |
| `ui/src/main.ts` | 488 | `file` |
| `ui/src/main.ts` | 492 | `requested` |
| `ui/src/main.ts` | 493 | `identity` |
| `ui/src/main.ts` | 496 | `object` |
| `ui/src/main.ts` | 498 | `candidate` |
| `ui/src/main.ts` | 499 | `validated` |
| `ui/src/main.ts` | 503 | `error` |
| `ui/src/main.ts` | 509 | `kind` |
| `ui/src/main.ts` | 510 | `event` |
| `ui/src/main.ts` | 511 | `input` |
| `ui/src/main.ts` | 512 | `file` |
| `ui/src/main.ts` | 516 | `downloadDraft` |
| `ui/src/main.ts` | 524 | `value` |
| `ui/src/main.ts` | 525 | `url` |
| `ui/src/main.ts` | 530 | `anchor` |
| `ui/src/main.ts` | 553 | `releaseFooter` |
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
| `tests/browser/import.spec.ts` | 7 | `Window` |
| `tests/browser/import.spec.ts` | 14 | `login` |
| `tests/browser/import.spec.ts` | 14 | `page` |
| `tests/browser/import.spec.ts` | 14 | `role` |
| `tests/browser/import.spec.ts` | 15 | `accounts` |
| `tests/browser/import.spec.ts` | 32 | `{ page, }` |
| `tests/browser/import.spec.ts` | 36 | `original` |
| `tests/browser/import.spec.ts` | 37 | `policy` |
| `tests/browser/import.spec.ts` | 39 | `rule` |
| `tests/browser/import.spec.ts` | 40 | `operation` |
| `tests/browser/import.spec.ts` | 42 | `[kind, value]` |
| `tests/browser/import.spec.ts` | 57 | `pending` |
| `tests/browser/import.spec.ts` | 61 | `file` |
| `tests/browser/import.spec.ts` | 74 | `retained` |
| `tests/browser/import.spec.ts` | 75 | `buffer` |
| `tests/browser/import.spec.ts` | 95 | `help` |
| `tests/browser/import.spec.ts` | 98 | `helpBox` |
| `tests/browser/import.spec.ts` | 113 | `{ page, }` |
| `tests/browser/import.spec.ts` | 118 | `original` |
| `tests/browser/import.spec.ts` | 122 | `resolve` |
| `tests/browser/import.spec.ts` | 122 | `reject` |
| `tests/browser/import.spec.ts` | 129 | `original` |
| `tests/browser/import.spec.ts` | 130 | `older` |
| `tests/browser/import.spec.ts` | 131 | `newer` |
| `tests/browser/import.spec.ts` | 132 | `hold` |
| `tests/browser/import.spec.ts` | 175 | `{ page, }` |
| `tests/browser/import.spec.ts` | 179 | `original` |
| `tests/browser/import.spec.ts` | 180 | `retained` |
| `tests/browser/workbench.spec.ts` | 6 | `login` |
| `tests/browser/workbench.spec.ts` | 6 | `page` |
| `tests/browser/workbench.spec.ts` | 6 | `role` |
| `tests/browser/workbench.spec.ts` | 7 | `credentials` |
| `tests/browser/workbench.spec.ts` | 20 | `{ page, }` |
| `tests/browser/workbench.spec.ts` | 24 | `original` |
| `tests/browser/workbench.spec.ts` | 25 | `draft` |
| `tests/browser/workbench.spec.ts` | 26 | `rule` |
| `tests/browser/workbench.spec.ts` | 40 | `pending` |
| `tests/browser/workbench.spec.ts` | 42 | `path` |
| `tests/browser/workbench.spec.ts` | 43 | `result` |
| `tests/browser/workbench.spec.ts` | 46 | `rule` |
| `tests/browser/workbench.spec.ts` | 56 | `{ page, }` |
| `tests/browser/workbench.spec.ts` | 69 | `download` |
| `tests/browser/workbench.spec.ts` | 74 | `[value, label]` |
| `tests/browser/workbench.spec.ts` | 95 | `changed` |
| `tests/browser/workbench.spec.ts` | 97 | `releaseReport` |
| `tests/browser/workbench.spec.ts` | 98 | `enteredReport` |
| `tests/browser/workbench.spec.ts` | 99 | `reportStarted` |
| `tests/browser/workbench.spec.ts` | 99 | `resolve` |
| `tests/browser/workbench.spec.ts` | 102 | `reportGate` |
| `tests/browser/workbench.spec.ts` | 102 | `resolve` |
| `tests/browser/workbench.spec.ts` | 107 | `route` |
| `tests/browser/workbench.spec.ts` | 127 | `{ page, }` |
| `tests/browser/workbench.spec.ts` | 133 | `historyButton` |
| `tests/browser/workbench.spec.ts` | 137 | `policy` |
| `tests/browser/workbench.spec.ts` | 148 | `currentReport` |
| `tests/browser/workbench.spec.ts` | 176 | `operatorReport` |
| `tests/browser/workbench.spec.ts` | 200 | `{ page, }` |
| `tests/browser/workbench.spec.ts` | 204 | `release` |
| `tests/browser/workbench.spec.ts` | 205 | `entered` |
| `tests/browser/workbench.spec.ts` | 206 | `started` |
| `tests/browser/workbench.spec.ts` | 206 | `resolve` |
| `tests/browser/workbench.spec.ts` | 209 | `gate` |
| `tests/browser/workbench.spec.ts` | 209 | `resolve` |
| `tests/browser/workbench.spec.ts` | 214 | `route` |
| `tests/browser/workbench.spec.ts` | 223 | `changed` |
| `tools/browser_checks.mjs` | 8 | `project` |
| `tools/browser_checks.mjs` | 9 | `result` |
| `tools/check_browser_host.mjs` | 9 | `engines` |
| `tools/check_browser_host.mjs` | 10 | `requested` |
| `tools/check_browser_host.mjs` | 12 | `name` |
| `tools/check_browser_host.mjs` | 13 | `key` |
| `tools/check_browser_host.mjs` | 19 | `lock` |
| `tools/check_browser_host.mjs` | 20 | `installed` |
| `tools/check_browser_host.mjs` | 27 | `temporary` |
| `tools/check_browser_host.mjs` | 31 | `name` |
| `tools/check_browser_host.mjs` | 32 | `engine` |
| `tools/check_browser_host.mjs` | 39 | `browser` |
| `tools/check_browser_host.mjs` | 41 | `page` |
| `tools/check_browser_host.test.mjs` | 7 | `refused` |
| `tools/check_browser_host.test.mjs` | 7 | `args` |
| `tools/check_browser_host.test.mjs` | 7 | `extraEnvironment` |
| `tools/check_browser_host.test.mjs` | 8 | `environment` |
| `tools/check_browser_host.test.mjs` | 11 | `child` |
| `tools/check_browser_host.test.mjs` | 31 | `key` |
| `tools/check_browser_host.test.mjs` | 35 | `value` |
| `tools/native_feature_smoke.mjs` | 8 | `[base, output]` |
| `tools/native_feature_smoke.mjs` | 10 | `origin` |
| `tools/native_feature_smoke.mjs` | 11 | `browser` |
| `tools/native_feature_smoke.mjs` | 12 | `context` |
| `tools/native_feature_smoke.mjs` | 17 | `page` |
| `tools/native_feature_smoke.mjs` | 18 | `errors` |
| `tools/native_feature_smoke.mjs` | 19 | `external` |
| `tools/native_feature_smoke.mjs` | 20 | `statuses` |
| `tools/native_feature_smoke.mjs` | 21 | `passed` |
| `tools/native_feature_smoke.mjs` | 22 | `response` |
| `tools/native_feature_smoke.mjs` | 29 | `error` |
| `tools/native_feature_smoke.mjs` | 30 | `request` |
| `tools/native_feature_smoke.mjs` | 39 | `login` |
| `tools/native_feature_smoke.mjs` | 39 | `role` |
| `tools/native_feature_smoke.mjs` | 51 | `logout` |
| `tools/native_feature_smoke.mjs` | 52 | `pending` |
| `tools/native_feature_smoke.mjs` | 53 | `response` |
| `tools/native_feature_smoke.mjs` | 63 | `importFile` |
| `tools/native_feature_smoke.mjs` | 63 | `kind` |
| `tools/native_feature_smoke.mjs` | 63 | `value` |
| `tools/native_feature_smoke.mjs` | 80 | `download` |
| `tools/native_feature_smoke.mjs` | 80 | `name` |
| `tools/native_feature_smoke.mjs` | 81 | `pending` |
| `tools/native_feature_smoke.mjs` | 83 | `file` |
| `tools/native_feature_smoke.mjs` | 91 | `original` |
| `tools/native_feature_smoke.mjs` | 96 | `valid` |
| `tools/native_feature_smoke.mjs` | 98 | `missing` |
| `tools/native_feature_smoke.mjs` | 100 | `item` |
| `tools/native_feature_smoke.mjs` | 111 | `evaluation` |
| `tools/native_feature_smoke.mjs` | 112 | `response` |
| `tools/native_feature_smoke.mjs` | 121 | `held` |
| `tools/native_feature_smoke.mjs` | 126 | `item` |
| `tools/native_feature_smoke.mjs` | 129 | `beforePreview` |
| `tools/native_feature_smoke.mjs` | 132 | `draft` |
| `tools/native_feature_smoke.mjs` | 134 | `rule` |
| `tools/native_feature_smoke.mjs` | 142 | `comparison` |
| `tools/native_feature_smoke.mjs` | 146 | `wind` |
| `tools/native_feature_smoke.mjs` | 146 | `item` |
| `tools/native_feature_smoke.mjs` | 159 | `prior` |
| `tools/native_feature_smoke.mjs` | 186 | `satisfied` |
| `tools/native_feature_smoke.mjs` | 188 | `item` |
| `tools/native_feature_smoke.mjs` | 218 | `reviewResponse` |
| `tools/native_feature_smoke.mjs` | 219 | `response` |
| `tools/native_feature_smoke.mjs` | 231 | `reviewed` |
| `tools/native_feature_smoke.mjs` | 239 | `region` |
| `tools/native_feature_smoke.mjs` | 246 | `element` |
| `tools/native_feature_smoke.mjs` | 252 | `element` |
| `tools/native_feature_smoke.mjs` | 272 | `cookies` |
| `tools/native_feature_smoke.mjs` | 302 | `diagnostics` |
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
