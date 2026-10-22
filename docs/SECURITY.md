# Threat model and privacy boundary

Jason Stys: assets, explicit organizational trust, controls and residual risks.

Assets: local account/password hashes, sessions, policy integrity, staff evidence, review/audit history and exports. Trust the workstation/OS/database owner, reviewed source/locks, official pinned OPA bytes and explicitly provisioned organizational administrators/reviewers. Operators are not trusted to inspect other operators' evidence or change policy. No role is trusted to turn an application acknowledgement into flight permission.

| Threat | Implemented control / evidence |
| --- | --- |
| Password disclosure/guessing | Argon2id64MiB/time3/parallelism1; no plaintext password persistence, generic invalid credentials,20 attempts/minute per direct client,1000client-row cap, maximum2 concurrent memory-hard verifications, bounded credential length. |
| Session theft/CSRF | Random256bit-class opaque tokens, only tokenSHA256 stored, one-hour absolute expiry, logout revocation, at most10 sessions/user, HttpOnly/SameSiteStrict cookie, exact Host/Origin and session CSRF on writes. No localStorage passwords or bearer tokens. |
| Privilege/object access | CLI-only account provisioning; admin-only policy publication; reviewer-only independent review; operators cannot read others' IDs/history/audit. Every endpoint rechecks server identity; UI disabling is not authorization. |
| Injection/execution | Closed finite typed contracts; parameterized SQL; no user code/queries/Rego/uploads; fixed OPA binary/query/policy paths, data stdin, no shell. Dynamic DOM/SVG content is not interpreted as HTML. HTTPS research links are never fetched by the service. |
| Unbounded work |256KiB body and5s body deadline;40rules/128claims; two native jobs and5s process timeout,128000character result cap; bounded history queries and launcher HTTP concurrency. Native binary itself is trusted, not arbitrary executable input. |
| False assurance/quality loss | Explicit review holds, contradictions retained, no implicit operation jurisdiction/framework, conditional applicability quality checks, complete result inventory, independent aggregate check and visible engine failure. Permanent non-authorization statement. |
| Stale/racing approval | Serialized write transactions, active-version compare-and-swap, policy recheck after evaluation, original snapshot content hashes, independent reviewer and no override of blocked/unknown/stale results. SQL immutability triggers; duplicate review rejected. |
| Browser injection/tracking | CSP default-none/self-only resources, no remote scripts/fonts/maps/ads/analytics, no-store, no-referrer, nosniff, DENY/frame-ancestors none and denied camera/mic/geolocation. |
| Supply chain | Hash-locked Python/npm, official OPA releaseSHA256 checked before execution, checksum-pinned official live OSV scanner with independently complete npm inventory, pip-audit, immutable Actions refs and no artifact/cache uploads. |

SQLite and exports are **not encrypted by this app**. Use a protected workstation, appropriate OS permissions/full-disk encryption and encrypted backups if needed. Designated staff can read organizational evidence according to their provisioned role; the public source author cannot remotely read it, and no telemetry channel exists. A machine/database administrator can access local data; content hashes/triggers are not an externally signed tamper-proof ledger. No software promises immunity from compromised OS/admin/browser extensions or other hostile local services.

Loopback HTTP is a deliberate local trust boundary, not a hosted account system. Cookie isolation is not port-based: trust other services running under the same local host, and do not use this lab with sensitive data on a shared/untrusted workstation. There is no TLS/public-host hardening, federation/MFA/password recovery, tenant isolation, encrypted object store, external audit service, real approval verifier or authoritative aviation feed. Do not tunnel/reverse-proxy/bind remotely. Those require a separately reviewed design and deployment authority.

The synthetic demo/test launcher creates random disposable staff credentials in ignored runtime files; these are not recommended production accounts. Production-like users should use the hidden-prompt CLI. Account creation does not send email, accept provider terms or transmit data externally. OSV/pip-audit are explicit development checks that contact advisory services with package identities; runtime evaluation remains offline.

Known-tool limitations: CodeQL covers Python/TypeScript, not Rego or vendor OPA internals. Rego has strict compiler/native tests and measured line coverage; OPA is a vendor binary with its own Go dependency supply chain, not claimed exhaustively audited here. Vulnerability scans are time-bounded evidence, not a guarantee. Report issues via root SECURITY.md; never publish private claims, passwords, tokens or unredacted exports in public issues.
