# Unpublished policy impact validation — 2026-11-09

Jason Stys: administrator-only configuration review without publication.

`workbench/impact.py` evaluates the exact same operation under active and draft
policies using the checksum-verified trusted OPA/Rego path. It preserves removed
and new check identities, configuration-only changes and decision/reason changes.
The export contains reproducible inputs, one content hash, both results and an
explicit unpublished/no-authorization notice. The existing immutable policies,
evaluations, reviews and audit are not mutated. Input JSON stays data, not Rego.

The API requires the admin role, real session CSRF and expected active version.
It checks version again after both calculations. Engine failures remain visible;
there is no satisfied fallback. Draft/edit races discard obsolete browser output.
The labeled comparison region is usable by assistive technology.

## Observed validation

- 86 Python tests, 98.78% branch-inclusive coverage; new impact module 100%.
  Actual OPA decisions on both sides match the independent Python rule oracle.
  Tests cover changed/renamed/removed/new/unchanged checks and input immutability.
- Real API tests prove operator/reviewer denial, CSRF rejection, stale versions,
  malformed extra fields, no database/history mutation, unavailable engine and
  actual concurrent policy publication rejection.
- 6 TypeScript tests at 100% helper coverage; strict production build and all
  16 Chromium/Firefox/WebKit/mobile journeys passed. They exercise actual draft
  edit, download, source hashes, no-publication and edit invalidation, plus the
  existing independent review, hostile text, privacy and WCAG gates.
- OPA format/check/test and coverage passed: authored Rego and tests 100% (90%
  gate unchanged). Maximum 40-rule/128-claim benchmark: 20 runs, median123.775ms,
  max200.930ms including checksum/process/compile/protocol checks on this PC.
- Exact locked Python advisory audit: no known vulnerabilities. Full live OSV
  npm inventory: 81/81 identities, zero findings. Ruff/format/navigation/hygiene
  checks and all existing acceptance thresholds remain required.

The unchanged Axe gate caught an invalid label on the initial output `div`; the
output now has a named region role and the full suite passed. Sandbox vendor
binary launch returned Windows DLL-relocation errors; identical fixed local OPA
checks passed with scoped execution permission, without machine configuration
changes. These are local results; parent publication CI remains separate.

## Limits

Configured checks cover a bounded organizational subset and self-reported
fictional evidence, not a complete/current legal assessment or independently
verified approval. No real aircraft, airspace authorization service, operational
flight, safety certification or weapon functionality is connected. Removing a
check is visible in the comparison and never grants external authority. Draft
results have no persisted review and must not be represented as saved evaluations.
