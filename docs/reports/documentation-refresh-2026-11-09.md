# Documentation refresh — 2026-11-09

By Jason Stys.

This documentation-only edition describes source `60a40fc4cbfe11cf0237dd7146e0b35cd660c32d`. It does not change application behavior, accounts, private data, installers or published releases.

## Published editions and completed review

| File | Bytes | SHA-256 | Reviewed scope |
| --- | ---: | --- | --- |
| [project-guide.docx](project-guide.docx) | 45748 | `81533085816e0ed6a7ce249df2f580c09161118bb4e2008ce143220163052c0a` | 6 pages, each viewed individually |

Word review checked plain black titles, readable pagination, whole table rows, source references, practical limits and absence of clipping or overflow. Render receipts were matched to the current DOCX digest before approval.

## Evidence and change boundary

- Functional baseline: `60a40fc4cbfe11cf0237dd7146e0b35cd660c32d`.
- Workflow observation: `2026-11-10T05:25:40.628667+00:00`; exact run URLs and source identities remain in [publications.json](publications.json).
- Local document-package validation verifies exact copied bytes, Office ZIP integrity, approved page/tab identities and internal documentation links. Repository-specific documentation and source-policy commands are run separately and recorded in the integration handoff.
- Source/index metadata is regenerated using the repository’s existing tools. Existing privacy, security, coverage and workflow gates are retained.
- PR and later main workflows must pass independently. This record does not claim future or unrun integration CI success.

## Interpretation

The Word files document the cited source; dated source reports retain their original execution scope. A passing workflow is distinct from completed analysis with zero findings, and neither establishes production suitability. Checksums identify exact bytes, not a signature or publisher attestation.

Use the [handbook](../handbook.md) to choose usage, design, security and test documentation. Keep editable Markdown and reviewed editions together; do not replace historical measurements with undated claims.

## Actual integration validation

98 Python tests passed with 98.78% combined coverage (90% floor), 6 TypeScript tests at 100% helper coverage, production build, Ruff/format, source maps and existing privacy/workflow checks. Twelve actual ZIP/privacy fixtures are included; no test was skipped. Hosted browser/native/security checks remain required.

Exact reviewed Office paths receive a bounded descriptor/ZIP XML and relationship reader. Unknown binary names still receive strict UTF-8 handling. Member/expanded-byte budgets, strict XML decoding and active/embedded payload rejection preserve the existing secret-content scan. The twelve independent actual-ZIP cases include both document and relationship credentials rejected through the genuine existing repository guard. No Office content is executed.
