# Drone Flight Policy Workbench handbook

By Jason Stys.

Compare active and draft policies using the same evidence and time, with exact native OPA inputs and failure states.

Compare active and draft policies using the same evidence and time, with exact native OPA inputs and failure states.

Supports controlled policy review without publishing a draft or treating a comparison as flight authorization.

## Read the documentation

| Edition | Audience and contents |
| --- | --- |
| [project-guide.docx](reports/project-guide.docx) | User and developer guide: purpose, current usage, design, boundaries and source references. |

The editable Markdown remains the maintenance source. The Word files are readable editions. See [publication identities and review](reports/publications.json) and the [documentation refresh record](reports/documentation-refresh-2026-11-09.md).

## Current usage and help

[README quick start](../README.md) is the entry point. Use the project-specific guides below before changing inputs, operating modes or deployment assumptions.

### Usage and operations

- [OPERATIONS](OPERATIONS.md)

### Design and contracts

- [API](API.md)
- [ARCHITECTURE](ARCHITECTURE.md)
- [RESEARCH](RESEARCH.md)

### Security and validation

- [SECURITY](SECURITY.md)
- [TESTING](TESTING.md)
- [VALIDATION](VALIDATION.md)

## Historical results and reproduction

The reviewed source is [`60a40fc4cbfe11cf0237dd7146e0b35cd660c32d`](https://github.com/JasonStys/drone-flight-policy-workbench/tree/60a40fc4cbfe11cf0237dd7146e0b35cd660c32d). The observed functional workflow baseline is `60a40fc4cbfe11cf0237dd7146e0b35cd660c32d`; those observations are recorded at `2026-11-10T05:25:40.628667+00:00`. They do not certify an unrun later revision.

- [Detailed recorded validation](reports/PRACTICAL_WORKFLOWS_20261109.md)
- [Current Actions](https://github.com/JasonStys/drone-flight-policy-workbench/actions) records later integration checks separately.
- Preserve dated measurements and follow the existing testing guide to reproduce them; a test-source inventory alone does not establish execution.

## Practical boundaries

- Bounded organizational checklist using fictional self-reported evidence, not complete/current law or verified approval.
- An unpublished comparison is not persisted human review and grants no flight or legal authorization.
- No real aircraft, surveillance or external authorization service is controlled. Source/package validation does not supply a public native desktop release.

## Maintaining these editions

Update the editable usage/design/test documents first. Rebuild and visually review every Word page and workbook tab before replacing an edition; verify the exact binary digests and evidence source in publications.json. Keep account data, logs with secrets, installed-app state and private test stores out of documentation. Source and release assets retain their existing security and licensing boundaries.
