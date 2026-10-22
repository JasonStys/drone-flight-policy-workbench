# Example organizational policy semantics

Jason Stys: scoped interpretation of synthetic rules, not an aviation-law database.

The baseline in `workbench/examples.py` is an original organizational training policy. Research references were checked2026-10-22UTC. They provide background, not evidence that an individual's real approval exists. The policy's validity900–2000 and operations' as-of1000 are a **synthetic exercise clock**, not dates of FAA approval or effective legal periods.

Configured checks include evidence currentness for credentials/registration, a recorded Remote ID applicability review, official restrictions check and observation plan. Controlled-airspace authorization, privacy planning/retention, sensitive-site permission and emergency coordination depend on explicit condition claims. A false, current, consistent, attested condition is not-applicable only; unknown applicability remains a review hold. Emergency claims never bypass authorization/evidence.

Organizational sample altitude100mAGL, wind8m/s and retention7days are **illustrative internal limits**, not legal maxima, manufacturer limits or a complete safety model. There is no terrain/weather feed, unit conversion or live authorization verification. Numbers are SI: altitude metres, wind metres/second, retention days. Numeric strings, booleans-as-numbers, NaN/infinity, negative/out-of-bounds values and unknown facts/rule types are rejected.

## Precedence

1. Wrong/unknown jurisdiction/framework or inactive/expired policy window: requires review for all checks; do not apply a policy outside its context.
2. Conditional applicability not supported by current, consistent, attested evidence: requires review. Explicit false condition: satisfied/not-applicable (not flight permission).
3. For the required fact, inspect **all supplied records** in this order: missing → conflicting values → unknown value → future observation → unattested → expired → stale → usable. Contradictory or obsolete supplied claims are not silently replaced by a convenient newest claim; submit a corrected new evaluation when appropriate. Observations exactly at max-age are current; expiry at as-of is expired.
4. Expired usable evidence blocks. Other quality problems require review. Usable values compare via typed equals/min/max, inclusive boundaries; failed comparison blocks.
5. Overall precedence: any blocked check → blocked; else any review hold → requires review; otherwise configured checks satisfied. Every rule must appear exactly once in engine output; invalid/incomplete/native-unavailable responses produce no saved assessment.

An administrator can change the configured subset, including loosening it; the version and content are preserved. Even an intentionally permissive policy's “satisfied” result is not a claim that every external obligation has been considered. Self-waiving conditional rules and contradictory simultaneously applicable bounds/equalities are rejected to reduce accidental errors. A reviewer cannot override blocked/unknown/stale evidence or acknowledge their own report. A recorded acknowledgement is not airworthiness or flight authorization.

Supplied `attested=true` means a person claims to have checked the record. No digital signature, government verification or source-document parsing is implemented. Source references are short labels, not uploaded private documents; URLs are HTTPS research links, never fetched by the service. Remote ID applicability exceptions, waivers, emergency arrangements, non-US rules and every other legal nuance require qualified human assessment outside this lab.
