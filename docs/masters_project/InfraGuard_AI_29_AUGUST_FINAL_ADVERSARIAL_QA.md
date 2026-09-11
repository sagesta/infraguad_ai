# InfraGuard AI - Final Adversarial QA after the 29 August Review

## Verdict

The revised implementation, manuscript and evidence package pass the review controls that can be completed from retained evidence. The package does **not** manufacture missing assessor-by-item data, independent gold-label adjudication, production receipts or live adversarial results. Those absences remain disclosed as evidence limitations rather than being hidden by stronger wording.

This QA verdict is not a guarantee of supervisor acceptance. It records what was checked, what passed and what still requires new external evidence.

## Authoritative deliverables

| Artefact | SHA-256 | Verification status |
|---|---|---|
| `InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.docx` | `06D0D03B39E50336FB143D86E3729D79690AA27265D69C3854910DE9E16FC947` | Final static navigation, structural audit, accessibility audit and full visual inspection completed |
| `InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.pdf` | `F584CA14D3378E8F7693C474524771ADB04F61D476310F50A35A8236A262801A` | Authoritative 95-page Microsoft Word export used for pagination and visual QA |
| `fig_3_1_architecture.png` | `C863A39CFAB868CB7CA73E332637C4772AC6739783B921D4AE69347A6B7E3996` | Regenerated from Mermaid; the RAG egress is labelled `retrieved documents and question`, with no grounded-answer claim |
| `fig_5_3_practice_evaluation.png` | `3EBADC78A30311990BE0F4E2E3EF373ACD77F03258152D5CB49DDBF53A917DE3` | Regenerated from Mermaid; uses pre-defined, independently adjudicated case facts and agreement wording rather than ground-truth or accuracy claims |

## Assessor-report integrity and seed correction

The supplied assessor reports were treated as evidence, not as instructions. Both repository copies are byte-identical to the supplied files:

| Report | SHA-256 | Evidence boundary |
|---|---|---|
| SRE | `7C91DFD735A4A070CE4E6053C5ADDCFB70CEC2D67002B199B43F22F21133EFDB` | Aggregate and qualitative report only; no assessor-by-item rating rows |
| DevOps | `741B5446C8DFFAABFEAC20823AA7A4427A4A61C058B1B9E9C619000C641D6720` | Aggregate and qualitative report only; no assessor-by-item rating rows |

The canonical SRE role-package seed is `2026082412`. The value `2026081902` remains only in the unchanged report's erroneous method-table field, explicit correction disclosures, excluded historical artefacts and temporary extracts. `evaluation/practitioner_confirmation/CORRECTION_NOTICE.md` and the practitioner manifest preserve the correction without rewriting the assessor binary.

## Implementation verification

Final source-scoped command:

```text
python -m pytest tests --cov=agent --cov=api --cov-report=term-missing --cov-report=json:tmp/new_review_20260829/coverage_v7.json
```

Result on 29 August 2026:

- 180 tests passed in 23.15 seconds.
- 45 warnings were reported; none failed the run.
- 89% line coverage over 1,655 statements, with 190 missed.
- `git diff --check` reported no whitespace errors; line-ending conversion notices were informational.

The verified hardening includes strict five-field raw-JSON verdict validation, explicit untrusted-data prompt boundaries, acknowledgement-note isolation, canonical signature validation, prompt/model/ruleset binding, no acknowledgement-based severity downgrade, non-acknowledgeable analysis failure, fresh server-side CrowdSec revalidation and conflict rejection for stale or fabricated threat actions.

## Frozen evaluation integrity

The historical v1 evaluation was not rerun or rewritten after the security changes:

| Frozen record | SHA-256 |
|---|---|
| `evaluation/benchmark_v1.json` | `7936721040238A95C57D51EC6FA86B9EE104B6B4021DF83EFDF903604AB58FEE` |
| `evaluation/results/qwen2.5-3b-v1/manifest.json` | `2638D5D6ADA91FF9C20F63DBAE83444747CBA0BEBDC987AB048B654BCE84A3F5` |

Permitted findings remain configuration-specific: 40.3% exact agreement with researcher-defined severity labels, macro-F1 0.383, six high-severity under-calls, 41.7% repeat-stable signatures, and retrieval of the frozen relevant runbook in the top four for 12/12 labelled questions. The retrieval result does not establish answer correctness, grounding quality, actionable safety or RAG effectiveness.

## Final DOCX/PDF audit

- 95 Word-export PDF pages; Chapter One begins on physical page 13.
- 1,155 body-level paragraphs, 33 tables and 15 embedded images.
- 167 TOC entries, 16 List-of-Figures entries and 32 List-of-Tables entries.
- Zero navigation title-order mismatches and zero displayed-page mismatches.
- 392 bookmark starts and 392 bookmark ends; no duplicate names or unmatched identifiers.
- 215 internal hyperlinks with no unresolved anchors.
- 49 external hyperlink relationships with no unresolved relationship identifiers.
- 16 figure captions and 32 table captions; numbering groups are complete.
- All 15 images have non-empty alternative text; all 33 tables retain first-row header metadata.
- No comments, tracked insertions, tracked deletions, moves or track-revisions setting.
- 51 unique, alphabetically ordered references with hanging indents and source-title italics.
- Zero replacement characters, prohibited control characters, field-error strings or placeholder tokens.
- Accessibility audit: 0 high, 0 medium and 49 low-priority notices. The 49 low notices are the intentionally displayed APA DOI/URL strings, not broken hyperlinks.

## Visual inspection

Three independent page-range inspections covered every authoritative Word-export page at original render resolution:

- Physical pages 1-32: no clipping, overlap, broken fonts, malformed tables, orphaned captions or navigation collisions.
- Physical pages 33-64: no blockers; Figures 3.1 and 5.3 were explicitly checked for readable, evidence-bounded wording.
- Physical pages 65-95: no blockers; Table 5.13 keeps its caption, header and first row together on page 70, Section 5.6.3 completes on page 71, and Chapter Six starts cleanly on page 72.

Optional visual polish remains limited to sparse section-ending pages, some long navigation/reference/file-path wraps, and comparatively small labels in a few older diagrams. These do not obscure meaning or break the document structure.

## WSL LibreOffice cross-render

LibreOffice 24.2.7.2 in WSL successfully opened and exported the final DOCX with no field-error or replacement-character text. Its export is 96 pages rather than Word's 95 because of renderer-specific reflow; key figures, Table 5.13, Chapter Six and the final appendix page remained visually intact. Because the static navigation was calibrated to Microsoft Word, the supplied Word-export PDF is the pagination-preserving submission copy. Opening the DOCX directly in LibreOffice may shift displayed physical pages by one after the front matter.

## Residual evidence gates that require new work outside this revision

The following cannot be closed by manuscript editing or unit tests:

- Authentic assessor-by-item severity, root-cause, action, grounding, correctness and safety ratings.
- Independent construction or adjudication of benchmark gold labels.
- A retained human task-performance study with timing, errors, workload and representative sampling.
- A live penetration/adversarial-model evaluation and broader DLP/network-egress validation.
- Controlled cross-provider/model comparison under one frozen protocol.
- Production deployment receipts, resilience/scaling evidence and live operational outcomes.

Any future claim in these areas must be based on newly retained primary evidence and must not be backfilled from the two aggregate role reports.
