# Test strategy and evidence denominators

Jason Stys: risk-based independent tests, real services and unweakened gates.

An additional real Uvicorn/loopback HTTP test varies forged `X-Forwarded-For` values across 21 requests and verifies that the actual direct-client limit still blocks the 21st attempt. No HTTP mock is used; the temporary listener is stopped and joined after the test. Both launchers disable proxy-header trust, and the CLI test asserts that setting.

Highest risks: false positive assurance, stale policy sign-off, type/unit confusion, missing/conflicting evidence, unauthorized report access, privilege escalation, input execution, snapshot corruption and inaccurate validation claims.

| Layer | Evidence |
| --- | --- |
| Native Rego | Four native decision-table groups: every evidence-quality state, conditional unknown/false/true, equals/min/max boundaries, context/window holds; strict compiler and format checks.90% line gate. Rego line coverage is not branch/semantic completeness. |
| Independent oracle |100 seeded real OPA runs vs a separately written imperative Python interpreter, checking every rule outcome/reason and aggregate; no reuse of production Rego decision functions. Explicit hand cases supplement random mutation. |
| Schema/units | Strict booleans/numbers/strings, null unknowns, finite bounds, nonnegative SI quantities, duplicate IDs, cardinality, future/reversed/expired dates, self-waiving conditions and contradictory simultaneous policy rules. |
| Identity/access | Actual Argon2/session flow, unknown/dummy users, role enforcement, cross-user ID/export/history isolation, CSRF/origin/Host, expiry/revocation, login attempts/session/verification capacity and no raw secret reflection. |
| SQL/workflow | Real SQLite transactions, exactly one winner for concurrent publication, rollback, immutable update/delete triggers, snapshot hashes, stale persistence, policy-version invalidation, independent review, no hold override/duplicate/self review. |
| CLI/install | Idempotent initialization, hidden password confirmation/mismatch, approved roles, bounded loopback port and server arguments. No tests install global software or repair Docker. |
| TypeScript | Pure status/count/review-eligibility helpers100% statements/branches/functions/lines; strict compiler plus unused local/parameter checks. DOM controller is covered through browsers, not included in the helper percentage. |
| Browser | Chromium/Firefox/WebKit and mobile WebKit, actual Python/SQLite/OPA: login, three statuses/four cases, exports, invalid JSON, read-only policy for operators, admin versioning, historical staleness, independent positive acknowledgement, hold refusal, WCAG2A/AA/2.1AA axe and mobile overflow. In-flight draft regressions pause then forward real requests; no fabricated responses/retries. |
| Dependency/security | Full Python development hash-lock pip-audit; official SHA-pinned live OSV over81 resolved npm identities with independent inventory/zero-finding gate and15 report-policy regression cases. No suppressions; unavailable/partial scans fail. Python/TypeScript CodeQL security-and-quality. |
| Reproducibility/performance | Python 3.12/3.14 on Ubuntu 24.04 plus3.14 Windows/macOS; Node.js 24; pinned OPA 1.21.3. Full 40-rule/128-claim native workload includes SHA256/process/compile/result overhead. JS40 KB/CSS12 KB gzip budgets. Documentation freshness/pinned workflow/source-secret checks. |

Package branch-aware Python coverage gate 90%, including CLI. Native Rego line gate 90%;100% measured lines do not prove every context/comparator/evidence combination. No aircraft, legal-provider, live feed, real emergency or remote hosting tests are claimed. Model-quality tests cannot certify aviation safety or legal completeness.

Browser accounts/database live in a unique ignored UUID directory per invocation to avoid shared-state/throttle contamination when rerunning tests. They never touch `.runtime/workspace.sqlite3` or actual user credentials. Dedicated reviewers/admins are intentionally authorized to access organizational reports; operators are isolated from other operators.

Run all README gates from the root in the activated environment. Generate source/file navigation with`python tools/docs_index.py`; CI uses`--check` and cannot silently rewrite stale documentation. Native OPA test coverage JSON is generated privately under`.runtime/opa/coverage.json`, not uploaded. Workflow logs and versioned documentation hold public evidence; no Actions artifact/cache uploads.

See VALIDATION.md for executed results, measured timings, corrections and exact hosted run links. A deprecation warning from Starlette's currently compatible httpx-based test client may be visible; it is not suppressed or treated as a skipped test.
