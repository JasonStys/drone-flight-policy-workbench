# Local API and data contracts

Jason Stys: authenticated routes, error handling, units and immutable evidence.

Origin/Host must exactly match `http://127.0.0.1:8881` (or selected port). All writes require JSON and exact Origin; authenticated writes additionally require the current session's `X-CSRF-Token`. Cookies are HttpOnly/SameSiteStrict with one-hour absolute expiry; local HTTP is intentionally not a remotely usable TLS service. No CORS, public registration, web password reset or remote role administration exists.

| Endpoint | Authorization / response |
| --- | --- |
| `GET /`, `GET /healthz` | Fixed UI and non-sensitive liveness. Liveness does not assert OPA readiness. |
| `POST /api/login` | Bounded username/password, generic401, throttled429; returns own name/role/CSRF and opaque cookie. |
| `GET /api/me`, `POST /api/logout` | Resolve/revoke current server session; no raw bearer tokens or password hashes returned. |
| `GET /api/workspace` | Active policy/version plus own operator history, or organizational history/audit for designated admin/reviewer roles. |
| `GET /api/examples` | Four fictional operation templates for signed-in staff. |
| `POST /api/policies` | Admin only: `{expected_version,policy}` → new immutable version; stale publication409. |
| `POST /api/evaluations` | Staff: `{version,operation}` → `{id,result}`. Real OPA; unchanged active version rechecked before persistence. |
| `GET /api/evaluations/{id}` | Creator/operator or designated admin/reviewer. Original policy/input/result/hash/time/review; stale marker and `flight_authorization:false`. Unknown/inaccessible objects404. |
| `POST /api/evaluations/{id}/review` | Independent reviewer only: `{decision:"acknowledge" or "reject",note}`. Current-version, one review; acknowledge requires satisfied result. No permission issued. |

Status codes:400untrustedHost,401invalid/expired/revoked session,403role/origin/CSRF,404not found or unauthorized object,405unsupported method,408body deadline,409stale/duplicate/ineligible review,413body>256 KiB,415wrong media type,422closed-contract/type/conflict/bounds validation,429login resource/throttle cap,503unavailable OPA/policy integrity/missing build. Input errors return locations/types and generic explanation, never submitted passwords/evidence values.

See exact schemas in `workbench/models.py`. Labels are bounded ASCII alphanumeric/spaces/underscore/hyphen/dot; unknown keys and coercion are rejected. Policy rules1–40; claims0–128; duplicate IDs rejected. Numeric quantities0–100000; clocks integer0–4e9. Fact names define units/dimensions. Evidence includes id/fact/value/source_ref/observed_s/expires_s/attested(defaultfalse). Unknown values useJSONnull. Operation jurisdiction/framework defaultsUNKNOWN, never inferred. Supported example policy context isUS/PART_107 only; other/unknown operations remain for review.

Rules include id/title/fact/comparator/expected/max_age_s1–86400, optional boolean when_fact/when_value, HTTPS research URL and reference. Policy has a name and ordered validity window. Arbitrary code, executable expressions, uploads or fetch targets are not accepted. All provided claims must be consistent/current under the documented precedence, not merely the newest.

Native OPA query is fixed: `data.flight.result`, with only reviewed `policies/flight.rego` loaded; input is JSON on stdin. Python verifies pinned vendor bytes before execution, process exit/size/timeout, result shape, unique complete rule IDs, status/reason vocabulary and independently recomputed overall hold precedence. No shell or arbitrary query/path is accepted from HTTP. Evidence snapshots include SHA256 content identities, not digital signatures; the host remains trusted.
