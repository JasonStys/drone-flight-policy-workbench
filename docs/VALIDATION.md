# Validation report

Jason Stys: measured execution evidence, scope limits and transparent hosted verification.

## Storage before Actions

2026-10-21T20:52:39-07:00:99repositories,62,959,952 live artifact bytes (~63.0MB decimal), private-repository artifact bytes0, separate caches8,185,324,614 bytes (~8.19GB). Quota percentage unavailable, not0%. Nothing deleted or retention-adjusted. These workflows upload no artifacts/caches.

## Executed local checks

Windows11 build26300, Python3.14.6, Node24.18.1, checksum-verified official OPA1.21.3. Actual OPA and SQLite are used in oracle/API/browser tests; no mocked success replaces them.

- Native Rego format/strict compile/four decision-table groups passed; measured100% line coverage for both production policy and test file, unchanged90% gate. No branch-coverage claim.
- Python:83 tests passed;98.71% branch-aware package coverage (472statements/148branches;3 statements and5 partial branches missed). Unchanged90% gate. Authentication and persistence modules measured100% in this run; package percentage includes the CLI. One visible Starlette test-client deprecation warning, no skipped tests.
- Independent seeded oracle runs100 varied actual OPA evaluations plus explicit edge/boundary cases.
- TypeScript helpers:6 tests pass;100% statements/branches/functions/lines (6statements/6branches/5functions/6lines). DOM controller excluded from that helper denominator; browser journeys exercise it.
- Browser:12 actual-service journeys across Chromium/Firefox/WebKit/mobile passed, including successful independent acknowledgement, stale/blocked refusal, exports, invalidation and paused-then-forwarded real request races; no retries.
- Live OSV:81/81 locked npm package identities scanned,0findings; full Python development hash-lock pip-audit:0known vulnerabilities. No advisory suppression or unavailable-as-pass behavior.
- Full40rule/128claim benchmark,20 actual calls: median103.553ms, max150.326ms, including binarySHA256, process launch, compile/evaluate and result validation. Machine-specific, not hard-real-time or flight-safety assurance.
- Strict TypeScript/unused-local/parameter checks and production build passed. Shipped JS5193gzip bytes (budget40000), CSS1468gzip bytes (budget12000). Ruff lint/format, Prettier, source/file navigation and public-source/pinned-CI checks passed.

## Review-driven protections

Omitted operation context staysUNKNOWN. Every supplied claim is considered; contradictions are not silently overwritten. Self-waiving conditional rules are rejected. Concurrent policy publication invalidates in-flight persistence and old review eligibility. UI draft revisions guard both the initial evaluation request and final report GET; historical/review loads use the same guard. Late responses cannot restore obsolete evidence or overwrite edits. An administrator's draft retains its original policy-version base across automatic history refreshes, avoiding accidental stale-write version laundering. Independent acknowledgement is not flight authorization. Password verification is bounded to two memory-hard operations concurrently. Browser runs use distinct private databases/credentials instead of sharing prior authentication throttles/history.

## Hosted status

Publishing/hosted checks remain a gate; no unexecuted hosted result is claimed here. Final implementation and documentation commits will be checked and linked after completion. Current local test-client deprecation warnings are visible, not suppressed. This lab is not certified, operationally approved, a legal-compliance guarantee or a remotely hosted product.
