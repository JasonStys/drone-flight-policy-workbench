# Architecture and ADR-001

Jason Stys: accepted local policy-as-code architecture, bounded requirements and trade-offs.

## Requirements and flow

`Authenticated operator → bounded typed operation + expected policy version → checksum-verified OPA/Rego → complete-result validation → atomic immutable SQLite snapshot → source-linked UI → independent reviewer`.

Administrators publish data-only policy versions with compare-and-swap against the expected active version. Evaluation occurs outside the write transaction; saving reacquires a transaction and rejects if the active policy changed. Review checks the original snapshot hash, current active version, reviewer identity, result status and prior-review absence within one serialized write transaction. Publishing does not delete history; old reports/reviews become explicitly stale. No operation dispatch, legal approval or override endpoint exists.

## ADR-001 — Rego decisions, Python boundary, SQLite evidence, TypeScript UI

Status: Accepted. Date:2026-10-22. Decider: Jason Stys (portfolio lab implementation).

Context: express explainable versioned checks without inventing legal certainty or duplicating a full flight controller. Policy decisions need independent validation and traceable input/version identities. Host is a trusted single-organization workstation, not a public service.

Decision: trusted Rego handles evidence quality, applicability, comparisons and aggregation. Python/Pydantic handles strict types, SI units, contradictions, native-process boundaries and role/object authorization. SQLite serializes small local state changes; SQL triggers guard policy/evaluation/review immutability. TypeScript renders inert text and manages draft/current/historical states.

Alternatives: pure Python would reduce tool setup but miss meaningful policy-as-code evidence; arbitrary uploaded Rego would introduce executable-policy risk; PostgreSQL and cloud services would add infrastructure without a current multi-host need. No AI is necessary for deterministic policy evaluation.

Trade-offs/consequences: OPA must be installed once from the pinned official release; its checksum is verified for each invocation, with startup/compile/hash overhead measured. Fixed-process evaluation makes failure visible and isolates trusted policy code, but is not a sandbox for arbitrary policy code. SQLite is suitable for this bounded local workspace, not multi-region scale. Authentication is local and OS-owned, not federation or multi-tenancy. Revisit TLS, identity, storage encryption, external audit, approvals/legal models and authoritative feed provenance before any separately approved hosting project.

## Data and complexity

Maximum40rules,128claims,256KiBHTTPbody; five-second body/process deadlines; two native evaluations and two Argon2 verifications concurrently. Argon2id uses64MiB/time-cost3/parallelism1 per hash. At most10 active sessions per user, one-hour absolute expiry,20 sign-in attempts/minute per direct client and1000 attempt-client rows; expired attempts/sessions are cleaned by sign-in. UI history queries cap30reports/60audit rows. Schema enforces roles, FKs, unique review/evaluation and immutable historical rows. Parameterized SQL prevents imported values becoming queries.

Input policy validation is `O(R²)` withR≤40; conceptual evidence checking is `O(R×E)` withE≤128 (OPA may memoize/optimize repeated lookups). Persistence is indexed by user/id for history; output/storage per report is `O(R+E)`. Report export includes original policy and evidence, not just totals. Hashes detect accidental corruption; they are not externally signed attestations or protection against a malicious host administrator.

Local files contain sensitive account/evidence state and must be protected by OS permissions and full-disk encryption where appropriate. Only explicitly provisioned organizational reviewers/admins can read others' reports; operators cannot. Public source contains synthetic fixtures only. Exported JSON stays local and must be protected by its recipient.
