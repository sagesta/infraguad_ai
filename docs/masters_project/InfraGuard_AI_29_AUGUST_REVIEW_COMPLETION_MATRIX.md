# InfraGuard AI - 29 August Review Completion Matrix

This matrix tracks every material requirement in the new supervisor review. “Completed” means the revised artefact addresses the manuscript or software-control requirement; it does not imply that missing external evidence has been created.

| Review requirement | Revision implemented | Evidence location | Status / residual boundary |
|---|---|---|---|
| Separate verification and validation | Defines both terms and classifies software, model/retrieval, qualitative practitioner, SUS, and governance evidence | Chapter 5 opening and Section 5.1 | Completed |
| Make human assessment recomputable | Removed unrecomputable means, rankings, agreement, kappas, and numeric RAG comparison from primary findings; retained reports as qualitative material | Sections 3.1.6, 5.4.2.4-5.4.2.6, 5.6, 6.2, 6.3, Appendix E; Tables 5.8-5.10 and E.5 | Safest completed fallback; original item-level records still unavailable |
| Document gold-label construction | States researcher authorship, pre-execution freeze, policy, lack of independent adjudication, single-primary-label rule, C20 sensitivity, and agreement meaning | Appendix E.1-E.3 and Table E.5 | Completed disclosure; no independent label validation claimed |
| Reframe RAG findings | Separates retrieval relevance, grounding/traceability, answer correctness, and actionable safety; keeps only `12/12` top-four retrieval as quantitative | Sections 2.1.5, 5.4.2.3, 5.4.2.5, Appendix E.4; Table 5.9 | Completed; human correctness/safety comparison unresolved |
| Add LLM-specific security analysis | Covers direct/indirect injection, exfiltration, poisoned evidence, output manipulation, unsafe action, privilege, acknowledgement poisoning, and supply-chain drift | Section 4.3.8 | Completed threat analysis; no penetration test or live red-team claim |
| Add cloud-LLM data flow | New source-controlled figure identifies host/cloud boundary, egress, return, local validation/storage, provider exposure, local Ollama path, and legal/organisational obligations | Figure 4.5 and Mermaid source | Completed |
| Clarify nature of contribution | Adds direct “What is new?” answer and separates conceptual, architectural, engineering, implemented-construct, and empirical contributions | Section 1.2.2 and Chapter 6.3 | Completed |
| Strengthen Chapter Two synthesis | Compresses the 13-study matrix and makes the primary methodology/governance hierarchy explicit | Sections 2.1.8 and 2.2; Table 2.1 | Completed |
| State requirements provenance | Retains unequivocal researcher-derived requirements disclosure; evaluation participants are not described as requirements sources | Section 3.2 and Table 3.2 | Completed; no retrospective stakeholder claim |
| Simplify research questions | Replaces RQ4a/RQ4b/RQ4c with one RQ4 and propagates five clean RQs through alignment and conclusions | Sections 1.3.2, 3.1.4, 6.2.1; Table 3.1 | Completed |
| Elevate signature instability | Retains `10/24`/`41.7%` as a central finding and states that model-generated identity is insufficiently stable | Sections 2.1.6, 4.4.3, 5.6.2, 6.2 | Completed |
| Distinguish provider support from evaluation | Adds explicit interface-versus-evidence table | Table 5.13 and Section 5.6.1 | Completed; only qwen2.5:3b has controlled retained model evidence |
| Keep SUS bounded | Retains item-level complete-case calculation and favourable perceived-usability interpretation only | Section 5.4.3 and Appendix D | Completed |
| Add post-review implementation hardening | Strict verdict validation, untrusted telemetry/runbook boundaries, note isolation, acknowledgement ruleset versioning, non-acknowledgeable pipeline failure, fresh server-side CrowdSec verification, and adversarial software tests | Agent/API source and source-scoped tests | 180 passed; 45 dependency warnings; 89% line coverage (1,655 statements; 190 missed); software verification only |
| Preserve frozen benchmark | Keeps v1 results immutable and explicitly separates them from post-benchmark code | Section 5.4.2, Table 5.13, Appendix E.7 and Table E.5 | Completed; new code requires a future v2 model run |
| Reduce abstract density | Keeps five headline indicators: 180 tests, 89% coverage, 40.3% researcher-label agreement, 41.7% repeat-stable signatures, and 79.25 mean SUS; retains the top-four retrieval result in prose and removes assessor comparison | Abstract | Completed |
| Improve editorial economy | Centralises the evidence boundary at Chapter Five and shortens repeated local caveats | Chapters 5 and 6 | Completed; final adversarial wording scan passed |
| APA/reference audit | Reconciles citations and references; validates DOI/URL formats and hyperlink targets | Final QA records | PASS - 51 cited references; unique and alphabetically sorted; hanging indents and source-title italics present; all 49 external hyperlink relationships resolve. Raw DOI/URL display text is retained by APA convention and accounts for the 49 low-priority accessibility notices. |
| Navigation and layout audit | Refreshes TOC/lists/page numbers/bookmarks; renders and inspects every final page | Final DOCX/PDF QA records | PASS - the authoritative Microsoft Word export has 95 pages, all visually inspected; TOC/List of Figures/List of Tables counts 167/16/32 with zero title or page mismatches; 215 internal links resolve; no visual blockers. A WSL LibreOffice 24.2.7.2 cross-render produced 96 pages, so the supplied Word-export PDF is the pagination-preserving submission copy. |

## Assessor-report verification

| File | Supplied copy versus repository | Item-level score evidence |
|---|---|---|
| `InfraGuard_DevOps_Assessment_Report.docx` | Byte-identical; SHA-256 `741B5446C8DFFAABFEAC20823AA7A4427A4A61C058B1B9E9C619000C641D6720` | Aggregate and qualitative report only; no 72-row assessor ratings |
| `InfraGuard_SRE_Assessment_Report.docx` | Byte-identical; SHA-256 `7C91DFD735A4A070CE4E6053C5ADDCFB70CEC2D67002B199B43F22F21133EFDB`; sidecar preserves `2026082412` as authoritative without changing the report | Aggregate and qualitative report only; no 72-row assessor ratings; legacy method-table value `2026081902` is documented as a transcription error |

## Final acceptance rule

The package is ready only when all implemented items pass structural, citation, navigation, hyperlink, accessibility, software-test, and full-page visual QA. The absence of authentic assessor-by-item records must remain disclosed; it cannot be converted into a completed quantitative human study by wording changes.
