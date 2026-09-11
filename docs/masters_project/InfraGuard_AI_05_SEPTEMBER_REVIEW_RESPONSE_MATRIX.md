# InfraGuard AI: response to the 5 September review

Revision completed on 6 September 2026. The authorised editorial and methodological corrections have been applied to a separate manuscript. The 2 September baseline, application code, frozen benchmark records, practitioner reports and SUS evidence were preserved.

Revised manuscript: [InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_5_SEPTEMBER_REVIEW.docx](C:/Users/adebo/PROJECTS/infraguad_ai/docs/masters_project/InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_5_SEPTEMBER_REVIEW.docx).

Baseline: [Final manuscript with the previous minor revisions applied](C:/Users/adebo/PROJECTS/infraguad_ai/docs/masters_project/InfraGuard_AI_Masters_Project_FINAL_MINOR_REVISIONS_APPLIED.docx).

The review recommends acceptance with minor to moderate revisions. This matrix records the response to its recommendations; it does not represent a new supervisory or institutional approval.

## Response matrix

Section references identify the revised thesis; review section numbers are given beside each concern.

| Review concern | Disposition | Revised location | Response |
|---|---|---|---|
| Research-question scope (review §5) | Implemented | §1.3.2; Table 3.1; RO5 in §1.3.3 and Table 5.12; §6.2.1 | Split RQ4 into RQ4a software verification, RQ4b the frozen model/retrieval benchmark and RQ4c descriptive SUS. Synchronised the questions, methods, objective evidence and answers. |
| Analytical literature synthesis (§6.1, §33) | Implemented | §2.2.2; new Table 2.2 | Compared tasks, methods, evidence limitations and design implications across incident assistance, retrieval, memory/identity and human oversight. Preserved the existing comparative review and renumbered subsequent Chapter Two tables. |
| Requirement traceability (§9, §33) | Implemented | §3.2; Tables 3.3–3.5 | Preserved FR-01–FR-15 and NFR-01–NFR-14. Added an acceptance criterion, source/priority and implementation or test reference for all 29 requirements. Marked live or broader acceptance outcomes without completed verification. Clarified heartbeat scheduling and asynchronous runbook work. |
| Researcher-defined gold labels (§16, §32) | Implemented | §3.1.2; §5.4.2.2; §5.6.2; Appendix E.1 | Made the label-policy limitation explicit in the main methodology. The 40.3% result remains agreement with the frozen researcher-defined policy. Independent expert adjudication remains a subsequent-study requirement. |
| Signature instability as a finding (§11, §32) | Implemented | §4.4; §5.6.1–5.6.2; §6.3; §6.4.3 | Elevated 10/24 repeat-stable signatures (41.7%) into a configuration-specific design finding about durable acknowledgement. Deterministic telemetry-derived identity remains a proposed architecture to evaluate. |
| Risk from severity errors (§17, §33) | Implemented | §5.4.2.2; §5.6.2 | Distinguished 8/24 exact high-class recall (33.3%) from 24/30 combined high/critical detection (80.0%). Explained the six under-calls as repeated outputs from C15 and C17, and the safeguard’s reliance on predicted severity. These calculations use existing rows; no new experiment or observed suppression event is claimed. |
| RAG claim boundary (§18, §32) | Implemented and retained | Abstract; §2.1.5; §5.4.2.3–5.4.2.5; §6.2.1; Appendix E.4 | Kept 12/12 top-four retrieval separate from grounding, correctness, actionable safety and a causal RAG benefit. Clarified the public item-level rating gap across the relevant sections. |
| Descriptive SUS interpretation (§20, §32) | Retained and tightened | Abstract; §3.1.3; §5.4.3; §6.2.1; Appendix D | Preserved 11 consented submissions, 10 complete responses, P9’s exclusion and mean 79.25. The interpretation remains favourable perceived usability within the convenience sample, without a population, workload or task-performance claim. |
| Software-verification chronology and scope (§14, §28) | Implemented | Abstract; §5.2; Table 5.1; §5.6.1; §6.2.1; Table E.5 | Added the dated 2 September repeat-verification row. Preserved the 29 August figure and the separate frozen 18 August benchmark. The 180 tests and 89% coverage remain a dated local working-tree receipt. |
| 89% versus 100% coverage (§22, §28, §32) | Implemented | §6.4.2; Figure 5.1 and Table 5.1 retained | Specified 100% for the selected modules and placed the recorded overall 89% in the same recommendation. The revision does not convert the overall coverage result to 100%. |
| Practitioner provenance (§19, §28) | Implemented | §3.1.3; §5.4.2.4–5.4.2.6; §5.6.2; Appendix E.3/E.7; Appendix F | Distinguished supplied DevOps/SRE reports, blank public A/B templates, reported confidential records and specific simulation-labelled development scores. Report integrity, human participation and public recomputability are treated as separate questions. No assessor means, kappas or reconstructed ratings were introduced. |
| Contribution and novelty (§7, §21, §30, §34) | Implemented | §1.2.1–1.2.2; §6.2–6.3 | Used a consistent governance-by-design reference-framework contribution and separated the implemented construct, engineering implementation and configuration-specific empirical findings. |
| Security controls and assurance (§13, §33) | Retained | §4.3; Table 4.3; §6.4.2 | Preserved the distinction between implemented controls, tested software paths and uncompleted adversarial or independent security assurance. A new penetration test was not represented as completed. |
| Abstract (§24, §33) | Implemented | Abstract | Reordered the problem, artefact, principal evidence and contribution. Removed detailed assessor-file provenance from the abstract while retaining concise study boundaries. It remains on one page. |
| Optional title shortening (§4) | Existing title retained | Title page and front matter | Preserved the existing project title and institutional front matter. The review described title shortening as an editorial option. |
| Repetition and terminology (§27–§28, §33) | Implemented | Abstract; Chapters One, Two, Five and Six; Appendix F | Shortened repeated caveats, retained qualifications next to standalone numerical claims, and synchronised RQ labels, model names, dates and evidence terminology. |
| Reference style and accuracy (§26, §32) | Implemented | References; cited discussion in §2.2.2 | Audited all 51 reference entries and their in-text keys. Corrected the Buçinca et al. venue and DOI; standardised the preprint punctuation. Preserved valid distinctions between papers, documentation and legal sources. |
| Figures, tables and navigation (§25, §33) | Implemented | Figure 3.7; Tables 2.2 and 3.5; contents, lists and Appendix F navigation | Enlarged the state-machine labels while retaining the code-defined transitions. Refreshed all 200 navigation entries, repaired five missing Appendix F links, kept table headers with their first data rows, and checked the complete rendered manuscript. |

## Evidence preserved

The frozen qwen2.5:3b benchmark still contains 24 scenarios repeated three times: 72 incident responses, 29/72 exact researcher-label matches (40.3%), macro-F1 0.383 and 10/24 scenarios with repeat-stable signatures (41.7%). The RAG comparison retains 12 questions, 36 RAG generations and 36 no-RAG generations, with 12/12 top-four retrieval. The separate SUS analysis retains 10 complete responses from 11 consented submissions and mean 79.25.

The newly explained 80.0% combined high/critical recall and 20.0% under-call share are descriptive calculations from the existing confusion matrix. No benchmark labels, response rows, human ratings or software-test results were manufactured or replaced.

The dated software receipt remains 180 tests and 89% overall source-scoped coverage for the 2 September local working tree. This manuscript revision did not rerun the application suite or the model benchmark.

## Items retained as further research

Independent expert label adjudication, larger practitioner panels, original item-level answer-quality ratings, cross-model comparisons, field studies, task timing and workload measurement, and adversarial security experiments remain specified future work. Deterministic telemetry-derived acknowledgement identity is a proposed implementation to evaluate. If original private examiner ratings are verified separately, their provenance and recomputed results can be documented without changing the frozen benchmark retrospectively.

## Reference audit

The corrected Buçinca et al. article is in *Proceedings of the ACM on Human-Computer Interaction*, 5(CSCW1), Article 188, DOI [10.1145/3449287](https://doi.org/10.1145/3449287), confirmed against the [authors’ publication copy](https://kgajos.seas.harvard.edu/papers/bucinca21trust.pdf). The former DOI identified a different article. Hevner et al.’s 75–105 page range was retained after checking the [primary issue record](https://www.jstor.org/stable/i25148619). Mulligan and Bamberger’s existing DOI was retained; it resolves to the [Berkeley Law record](https://lawcat.berkeley.edu/record/1128572).

Publisher access restrictions affected some automated landing-page requests. Registered metadata and primary author, institutional or official documentation sources were used where available; a blocked landing page was not treated as proof of a broken reference. All 51 expected reference keys were found in the manuscript and no unmatched prose citation keys were detected by the structural audit.

## Final document checks

- 103 A4 pages rendered and visually reviewed, including front matter, references and appendices.
- 200 contents/list entries matched the final page map and linked to the correct heading or caption.
- All 29 requirement IDs have a populated acceptance and verification entry.
- 51 references retained; the original empirical and protocol tables checked during validation were unchanged.
- Figure 3.7 was regenerated for readable labels; the other 14 embedded figures and the conceptual-framework table were preserved.
- No tracked changes, reviewer comments, unresolved internal links, blank rendered pages, replacement characters or page-edge clipping were found.
- Microsoft Word exported the final PDF proof; the bundled Python PDF runtime generated the page images. The packaged document renderer was attempted but had no bundled LibreOffice executable on this Windows installation. Proof files remain internal revision records.

Pagination and visual checks apply to this saved Word copy. There is no new physical-print or production-system evaluation associated with the revision.

## File integrity

| File | SHA-256 |
|---|---|
| Attached review | `810b1a1f05138ecd05affdb1daf026ef8abb5e621a991a935c8de9522a8415e7` |
| Preserved 2 September baseline | `f1bcb22ec8adf96369d58b70da76d4509be01bfa9343de2a8f5cdd51c7128f44` |
| Revised manuscript | `482d4bc758461673167733f7c8bcb123df939937c26d30e04ba401e9eb86e6ee` |
