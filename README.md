# Drone Flight Policy Workbench

Jason Stys: a source-linked, versioned **synthetic preflight and ethical-use review application**. It makes missing evidence visible, preserves the policy behind every result, and prevents human acknowledgement from silently overriding a hold.

[Validation](https://github.com/JasonStys/drone-flight-policy-workbench/actions/workflows/validate.yml) · [CodeQL](https://github.com/JasonStys/drone-flight-policy-workbench/actions/workflows/codeql.yml) · [Architecture](docs/ARCHITECTURE.md) · [Help](docs/OPERATIONS.md) · [Measured results](docs/VALIDATION.md)

## What it does

An operator submits a fictional proposed operation and structured claims about credentials, registration, Remote ID applicability, authorization evidence, restrictions, observation plans, privacy, site permission, emergency coordination and organizational limits. A real, checksum-verified **Open Policy Agent (OPA)** process evaluates trusted **Rego** against a bounded, data-only policy. Python validates types/units, stores immutable snapshots in SQLite, and enforces roles and independent review. TypeScript/HTML/CSS provides the browser interface.

Each check returns **satisfied**, **blocked**, or **requires review**, with a precise reason and dated research reference. No result is flight permission, a complete legal assessment or a safe-to-fly determination. The app never contacts FAA authorization services or verifies that an actual credential/approval exists.

### Major features

| Feature | Implemented behavior |
| --- | --- |
| Configurable organizational policy | Admin-only publication of immutable versions; typed equals/min/max rules, conditional applicability, SI quantities, policy-validity and evidence-freshness windows. Contradictory rules are rejected. |
| Conservative evidence handling | Missing, unknown, conflicting, future, unattested and stale claims remain review holds. Expired usable evidence or a failed configured comparison blocks that check. Every supplied claim is considered; contradictory history is not silently discarded. |
| Roles and private accounts | CLI-provisioned administrator/operator/reviewer roles, Argon2id password hashes, hashed opaque sessions, absolute expiry, logout revocation, CSRF and exact same-origin/Host checks. |
| Independent review | Another designated reviewer may acknowledge only current-version satisfied evidence, or record a rejection. No override of blocked/unknown/stale results. Acknowledgement is **not external authorization**. |
| Reproducible evidence | Original policy/input/result, SHA256 content identity, actual UTC creation time, explicit synthetic exercise time, stale markers, review record, bounded history/audit and local JSON export. |
| Privacy/access boundaries | Operators see their own reports; designated organizational reviewers/admins see staff reports. No analytics, remote scripts, AI providers, raw flight logs, personal identifiers or external runtime requests. |
| Verification | Actual OPA decisions vs an independent Python oracle, native Rego line coverage, SQL transaction/race/immutability tests, account/object security and real-service desktop/mobile browser journeys. |

The four original examples are an infrastructure inspection, flood survey missing authorization evidence, sensitive-site inspection with a retention hold, and an emergency exercise with an expired registration-evidence record. Everything is fictional and geographically unlocated. Emergencies do not bypass requirements. Organizational example limits are not claimed to be legal thresholds.

## Run locally

Prerequisites: Python 3.12–3.14 and Node.js24. No Docker, API key, remote account or paid hosting required. Supported local service platforms are Windows x64, Linux x64/ARM64 and macOS x64/ARM64; CI checks Windows/Linux/macOS. Mobile browser rendering is tested, but no installed native/mobile package is provided.

Create/activate a normal Python environment:

```text
python -m venv .venv
```

Then, from the repository root with that environment activated:

```text
python -m pip install --require-hashes -r requirements-dev.lock
npm ci --ignore-scripts --no-audit
python tools/fetch_opa.py
npm run build
python -m workbench init
python -m workbench user local-admin --role admin
python -m workbench user local-operator --role operator
python -m workbench user local-reviewer --role reviewer
python -m workbench serve --port 8881
```

Passwords are entered through hidden local prompts, not command-line arguments. Open **http://127.0.0.1:8881/**. Sign in, evaluate an example, inspect each hold/source, and export the evidence. Sign out and use a different reviewer to acknowledge eligible evidence. Administrators can edit the complete data-only policy JSON and publish a new immutable version. [Step-by-step help](docs/OPERATIONS.md).

OPA v1.21.3 downloads only through the explicit setup command from the official vendor release and is SHA256-verified before every evaluation. Runtime evaluation is local/offline. `npm --no-audit` avoids the install-time advisory endpoint; the separate required live OSV gate below still verifies the complete lockfile inventory without suppressions.

## Test and validate

```text
python -m ruff format --check workbench tests tools
python -m ruff check workbench tests tools
python -m tools.opa_checks
python -m pytest --cov=workbench --cov-report=term-missing
npm run format:check
npm test
npm run build
python tools/docs_index.py --check
python tools/check_repo.py
python -m tools.benchmark
python -m pip_audit --disable-pip --no-deps -r requirements-dev.lock
python tools/audit_osv.py
npx playwright install chromium firefox webkit
npm run test:e2e
```

Build the UI and install OPA before Python HTTP tests. Linux browser dependencies may need Playwright's `--with-deps`. Browser tests create a unique ignored runtime database and random disposable staff credentials per run; they never use production accounts. Coverage gates are90% branch-aware Python,90% native Rego lines and100% presentation helpers. CI runs four OS/Python combinations, actual-service Chromium/Firefox/WebKit/mobile acceptance, and Python/TypeScript CodeQL. It uploads no Actions artifacts/caches. [Test plan](docs/TESTING.md), [validation report](docs/VALIDATION.md).

## Important limitations

This is an educational, single-organization **loopback-only lab**, not a hosted multi-tenant product, legal adviser, complete aviation-rule engine, identity/approval verifier or certified flight-safety system. It does not issue LAANC approval, receive/transmit Remote ID, control aircraft, infer live restrictions, collect footage or monitor real people. Supplied attestation is a human claim, not cryptographic proof or independent verification. All clocks and thresholds in examples are synthetic.

Real applicability and approvals must be checked separately with qualified personnel and current official sources: [FAA LAANC](https://www.faa.gov/uas/getting_started/laanc), [FAA Remote ID](https://www.faa.gov/uas/getting_started/remote_id), [NTIA voluntary privacy guidance](https://www.ntia.gov/other-publication/2016/multistakeholder-process-unmanned-aircraft-systems). No provider, regulator, employer or military endorsement is claimed. A complete deployment would require professional legal/operational review and a separate hosting/security design.

Local `.runtime/` databases, sessions, demo credentials, OPA binaries and exports are ignored by Git. SQLite is **not encrypted by this application**; protect the workstation and backups. The OS/database administrator and designated organizational reviewers remain trusted. No software can promise protection from its own host administrator. Do not expose this local service using LAN binding, tunnels or a reverse proxy.

## File and function guide

- `workbench/models.py`: finite closed contracts, dimensions, policy consistency and bounded evidence.
- `workbench/engine.py`: fixed OPA query, checksum verification, concurrency/timeout and complete-output gate.
- `policies/flight.rego`: evidence quality, applicability, comparisons and hold precedence; `flight_test.rego` native decision-table tests.
- `workbench/store.py` / `schema.sql`: atomic immutable versions, snapshots, independent review, scoped history and audit.
- `workbench/auth.py` / `api.py` / `__main__.py`: credentials/sessions, protected HTTP workflow and trusted CLI.
- `workbench/examples.py`: original policy and four synthetic scenarios.
- `ui/`: responsive TypeScript/HTML/CSS workflow, presentation helpers and local export.
- `tests/`: independent oracle, schema/security/CLI/SQL tests and actual-service browser acceptance.
- `tools/`: verified vendor setup, native coverage gate, live dependency scan, documentation/source hygiene, benchmark and isolated demo/test launcher.
- `.github/workflows/`: pinned least-privilege cross-platform validation and CodeQL.
- `docs/`: architecture/ADR, API, example-policy scope, help, threat model, testing, research and measured reports.

Every file is summarized in the [generated file catalog](docs/FILE_CATALOG.md). Source headers link to the [exact function/declaration/variable line map](docs/SOURCE_MAP.md); AST/lexical generation keeps navigation current instead of hard-coding stale header line numbers. Functions/classes and important policy sections have explanatory headers.

Created by **Jason Stys** · [GitHub / Contact](https://github.com/JasonStys) · [LinkedIn](https://www.linkedin.com/in/jason-stys-31b30b351/). MIT original source; dependencies and OPA retain their own licenses.
