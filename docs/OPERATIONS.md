# Setup, user help and recovery

Jason Stys: local-only operation, organizational access and evidence interpretation.

Follow README prerequisites and build commands. The supported launcher binds127.0.0.1 only and disables access logging. Local database defaults`.runtime/workspace.sqlite3`; Git ignores this directory and allDB/SQLite extensions. Keep production-like data out of this educational lab.

## First use

1. Install hash-locked dependencies and checksum-verified OPA, build the UI, then `python -m workbench init`.
2. Provision local staff with `python -m workbench user NAME --role admin`, `operator` or `reviewer`. Enter/confirm a14–128character password through the hidden prompt. Only the trusted OS operator can provision; no public signup/reset endpoint exists. Existing names cannot be silently overwritten.
3. Start `python -m workbench serve --port 8881`; open`http://127.0.0.1:8881/`. Sign in with the account you created.
4. Evaluate the infrastructure-inspection example. Inspect every rule, quality reason, conditional requirement and linked research reference. Satisfied means only the configured subset passed.
5. Select missing-approval/privacy-hold/expired-record examples to observe review/blocked states. EditJSON for other synthetic inputs. A new evaluation preserves a new immutable snapshot; edits clear the current report/export immediately. Time values are an explicit synthetic exercise clock.
6. Admins may edit policyJSON and publish against the active version. Policy fields are data, not Rego. Contradictions and stale concurrent publications fail visibly. Operators/reviewers see read-only policy fields; API permissions apply independently of UI controls.
7. Choose a historical report to inspect its **original** policy and stale marker. Export only through your authorized report view. The download includes all supplied synthetic claims, original policy and result; protect it locally.
8. Sign out and sign in as a different reviewer. A current, satisfied, unreviewed report from another staff member can be acknowledged; blocked/unknown may be rejected but not positively overridden. Stale reports require re-evaluation. Nothing dispatches aircraft or grants permission.

## Disposable demonstration and acceptance

`python -m tools.browser_server --directory .runtime/demo --port 8881` creates a separate synthetic sandbox with random test-only admin/operator/reviewer credentials in`.runtime/demo/credentials.json`. Read that file locally to sign in; it is never exposed by an endpoint, logged or committed. These are disposable demonstration accounts, not recommended real accounts. Tests use a unique UUID-named ignored directory per run and never touch your initialized workspace. Do not enter private information into a shared demo.

## Troubleshooting and maintenance

| Symptom | Action |
| --- | --- |
| OPA unavailable503 | Run explicit`python tools/fetch_opa.py`; checksum failure must be investigated, not bypassed. Run native checks. The app never downloads a substitute at runtime. |
| UI503 | `npm ci --ignore-scripts --no-audit` then`npm run build`. No separate Vite server required. |
| Login401/429 | Check exact local account; generic errors avoid account disclosure. Wait a minute after throttle, or until another password verification finishes. No web recovery bypass exists. |
| Validation422 | Correct unsupported types/units/fields, duplicate IDs, contradictory rules or reversed intervals. Input passwords/values are not echoed in errors. |
| Conflict409 | Refresh active policy and evaluate again. Old reports/reviews are preserved, never rewritten to match new policy. |
| Missing/inaccessible report404 | Operators only see their own evidence. Provision approved reviewers explicitly; don't remove access checks. |
| Engine busy503 | Two native jobs are already running; retry after completion. No silent positive result or cloud fallback. |
| Browser setup | Install official Playwright Chromium/Firefox/WebKit builds; Linux may require`--with-deps`. Native worker/OS runtime failures remain failures. |
| Audit provider unavailable | Re-run later; an unavailable/incomplete scan does not count as clean. No suppressions or gate lowering. |

Stop only your own foreground server withCtrl+C. Back up by stopping the server and copying the SQLite database plus any exports to a protected, separately named backup location. Restore into a **new** path with`--db PATH`; do not overwrite or delete your current evidence casually. SQLite is not encrypted here; use appropriate workstation/backup encryption and access control. History is bounded in UI queries, not automatically deleted from disk; plan local capacity and explicit retention with your organization before any real deployment.

Upgrade by reviewing source/locks, backing up, running every test gate, then rebuilding. Roll back to reviewed source plus a matching compatible protected backup at a new path. Schema version 1 has no automatic destructive migration. No installer, autoupdater, OS service, scheduled cleanup, Docker repair or paid resource is created. Public source is not a signed/certified application package.
