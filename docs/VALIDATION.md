# Validation report

Jason Stys: measured execution evidence, scope limits and transparent hosted verification.

## Storage before Actions

2026-10-21T20:52:39-07:00:99 repositories,62,959,952 live artifact bytes (~63.0 MB decimal), private-repository artifact bytes0, separate caches8,185,324,614 bytes (~8.19 GB). Quota percentage unavailable, not0%. Nothing deleted or retention-adjusted. These workflows upload no artifacts/caches.

## Executed local checks

Windows 11 build 26300, Python 3.14.6, Node.js 24.18.1, checksum-verified official OPA 1.21.3. Actual OPA and SQLite are used in oracle/API/browser tests; no mocked success replaces them.

- Native Rego format/strict compile/four decision-table groups passed; measured100% line coverage for both production policy and test file, unchanged90% gate. No branch-coverage claim.
- Python:83 tests passed;98.71% branch-aware package coverage (472 statements/148 branches; 3 statements and 5 partial branches missed). Unchanged90% gate. Authentication and persistence modules measured100% in this run; package percentage includes the CLI. One visible Starlette test-client deprecation warning, no skipped tests.
- Independent seeded oracle runs100 varied actual OPA evaluations plus explicit edge/boundary cases.
- TypeScript helpers:6 tests pass;100% statements/branches/functions/lines (6 statements/6 branches/5functions/6lines). DOM controller excluded from that helper denominator; browser journeys exercise it.
- Browser:12 actual-service journeys across Chromium/Firefox/WebKit/mobile passed, including successful independent acknowledgement, stale/blocked refusal, exports, invalidation and paused-then-forwarded real request races; no retries.
- Live OSV:81/81 locked npm package identities scanned,0 findings; full Python development hash-lock pip-audit:0 known vulnerabilities. No advisory suppression or unavailable-as-pass behavior.
- Full 40-rule/128-claim benchmark,20 actual calls: median 103.553 ms, max 150.326 ms, including binarySHA256, process launch, compile/evaluate and result validation. Machine-specific, not hard-real-time or flight-safety assurance.
- Strict TypeScript/unused-local/parameter checks and production build passed. Shipped JS5193gzip bytes (budget40000), CSS1468gzip bytes (budget12000). Ruff lint/format, Prettier, source/file navigation and public-source/pinned-CI checks passed.

## Review-driven protections

Omitted operation context staysUNKNOWN. Every supplied claim is considered; contradictions are not silently overwritten. Self-waiving conditional rules are rejected. Concurrent policy publication invalidates in-flight persistence and old review eligibility. UI draft revisions guard both the initial evaluation request and final report GET; historical/review loads use the same guard. Late responses cannot restore obsolete evidence or overwrite edits. An administrator's draft retains its original policy-version base across automatic history refreshes, avoiding accidental stale-write version laundering. Independent acknowledgement is not flight authorization. Password verification is bounded to two memory-hard operations concurrently. Browser runs use distinct private databases/credentials instead of sharing prior authentication throttles/history.

## Hosted status

Reviewed implementation **`bdab705166e8e858cda24b92afeaae74eeca61ff`**:

- [Validation 39722371377](https://github.com/JasonStys/drone-flight-policy-workbench/actions/runs/39722371377): **all five jobs passed** — Ubuntu 24.04/Python 3.12, Ubuntu 24.04/Python 3.14, Windows/Python 3.14, macOS/Python 3.14, and actual OPA-backed Chromium/Firefox/WebKit/mobile browser acceptance. No failed or skipped jobs, coverage reductions or retries-to-green.
- [CodeQL 39722371320](https://github.com/JasonStys/drone-flight-policy-workbench/actions/runs/39722371320): **both Python and JavaScript/TypeScript security-and-quality jobs passed**; zero open code-scanning alerts when checked. Rego is covered by strict/native/oracle checks, not these CodeQL jobs.
- Main and origin/main matched the reviewed implementation. This subsequent documentation-only commit records the immutable run links, proofreads the guides, and is also subject to the same tests. The [latest main-branch runs](https://github.com/JasonStys/drone-flight-policy-workbench/actions?query=branch%3Amain) show its final status without pretending a run can contain its own future ID.

Storage recheck 2026-10-21T21:27:22-07:00: 100 repositories; still 62,959,952 live artifact bytes and 8,185,324,614 separate cache bytes. Quota percentage unavailable. This repository's APIs returned **0 artifacts / 0 bytes** and **0 caches / 0 bytes**. Nothing deleted, archived, retention-adjusted or billed through a new hosting service.

Current local test-client deprecation warnings are visible, not suppressed. This lab is not certified, operationally approved, a legal-compliance guarantee or a remotely hosted product.
