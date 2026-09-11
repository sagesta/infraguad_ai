# InfraGuard AI review assessment and revision plan

The attached review recommends acceptance with minor to moderate corrections. Comparing it with the latest manuscript shows that many of its methodological cautions are already stated explicitly. The remaining work is a focused revision of research-question structure, requirement traceability, literature synthesis, interpretation and consistency. The review places a larger independently labelled benchmark under a stronger subsequent study; it does not make that new study a condition of this revision.

This assessment was completed on 5 September 2026. The manuscript, application code and evidence records have not been edited.

## Documents compared

- Review: [Review with minor to moderate corrections](<C:/Users/adebo/AppData/Local/Packages/5319275A.WhatsAppDesktop_cv1g1gvanyjgm/LocalState/sessions/17CE65F44B978233D0743DAEBA9C04E5E863BDF3/transfers/2026-36/Review - Minor to Moderate Revision - InfraGuard_AI_Masters_Project_FINAL minor revised (1).docx>).
- Baseline: [InfraGuard AI final manuscript with minor revisions applied](C:/Users/adebo/PROJECTS/infraguad_ai/docs/masters_project/InfraGuard_AI_Masters_Project_FINAL_MINOR_REVISIONS_APPLIED.docx), last saved on 2 September 2026.
- Review SHA-256: `810b1a1f05138ecd05affdb1daf026ef8abb5e621a991a935c8de9522a8415e7`.
- Baseline SHA-256: `f1bcb22ec8adf96369d58b70da76d4509be01bfa9343de2a8f5cdd51c7128f44`.

The baseline hash matches the retained final rendering record. Relevant pages were checked in its 97-page PDF. Section numbers below refer to this manuscript, not an older adjudicated or reviewer-response copy. The review's recommendations are assessed as feedback, not treated as instructions to change the project automatically.

## What the comparison shows

| Review issue | What the latest manuscript contains | Recommended response |
|---|---|---|
| Broad RQ4 | Section 1.3.2 still combines software verification, model and retrieval results, and perceived usability in one question. Table 3.1 and Section 6.2.1 repeat that structure. | Split RQ4 conceptually into RQ4a, RQ4b and RQ4c, then update the alignment table and answers together. Keep RQ5 unchanged. |
| Analytical literature synthesis | Section 2.2.2 already has Known, Contested, Unresolved and Design implication paragraphs. | Strengthen the relationships between studies with a compact thematic matrix. Compare methods and evidence limitations, and support each claimed disagreement with the cited studies. |
| Requirement IDs and traceability | Tables 3.3 and 3.4 already contain FR-01 to FR-15 and NFR-01 to NFR-14. Section 3.2 gives sources, prioritisation and selected component/test traces. | Preserve those IDs. Add explicit acceptance criteria and verification references for each requirement, with source/rationale and priority where missing. Mark outcomes without completed evidence as unverified. |
| Researcher-defined labels | Sections 5.4.2.2, 5.6.2 and 5.6.3, Table 5.5 and Appendix E.1 already restrict 40.3% to agreement with the researcher's labels. Appendix E also explains C20 sensitivity. | Bring one clear statement into the main methodology and discussion. Do not relabel this metric as real-world diagnostic accuracy or change the frozen labels. |
| Signature instability | Section 4.4 explicitly calls 41.7% stability a central design finding. Sections 5.6.2, 6.2 and 6.4.3 also address identity instability and deterministic signatures. | Make the design lesson explicit in Section 5.6.1 and the contribution discussion. This is an emphasis change; deterministic identity remains a proposed next architecture. |
| Risk from severity errors | Section 5.4.2.2 already discusses zero warning recall, 33.3% exact high recall, under-calls and over-calls. It correctly identifies six repeated outputs from C15 and C17. | Add the distinction between exact-class recall and urgent-case detection described below. Connect misclassification to the limits of the acknowledgement safeguard. |
| RAG effectiveness | Sections 5.4.2.3 and 5.4.2.5 explicitly separate 12/12 top-four retrieval from grounding, correctness, safety and causal RAG benefit. | Retain this boundary and check it in the abstract and conclusion. A new RAG experiment is not needed to correct the wording. |
| SUS interpretation | Sections 3.1.3 and 5.4.3 and Appendix D already report 10 complete responses from 11 consented submissions, mean 79.25, and the convenience-sample limitation. | Preserve those numbers and describe favourable perceived usability within the sample. Avoid claims about workload, task performance or practitioner populations. |
| Local software-verification scope | The abstract, Section 5.2, conclusion and Table E.5 identify 180 tests and 89% coverage as a local working-tree result. | Apply the same scope to brief summaries such as Section 5.6.1. Align the chronology: Table 5.1 ends on 29 August, while Section 5.2 and Table E.5 also record the 2 September repeat verification. |
| 89% versus 100% coverage | Section 6.4.2 already names the modules to which 100% applies, while the overall result is 89%. | Add “selected modules” and the overall 89% figure to the same recommendation. This removes ambiguity; it is not evidence that the percentages themselves are wrong. |
| Practitioner evidence | Sections 3.1.3 and 5.4.2.4 and Appendix F exclude quantitative A1/A2 findings while retaining role reports. Repository metadata describes reported human scoring separately. | Reconcile the provenance wording using the file distinctions below. Neither the review nor a simulation label on a different file establishes that the supplied examiner reports were AI-generated. |
| Novelty and contribution | Sections 1.2.2 and 6.3 already distinguish conceptual, architectural, engineering and empirical contributions and limit uniqueness claims. | Keep this structure and use a consistent central contribution statement. A search found no “novel mechanism” claim in the main manuscript paragraphs. |
| Security assurance | Section 4.3.4 and Table 4.3 distinguish implemented controls from uncompleted adversarial and independent security assessment. | Preserve “security control implementation and design assessment” wording. This request does not require a new penetration test for the current editorial revision. |
| Abstract | The current abstract has 220 words excluding keywords and already fits on one page. | Improve its information order and remove detailed candidate-score provenance from the abstract. Keep the essential evidence boundaries in concise form and the full provenance discussion in Chapter Five and Appendix F. |
| Title length | The review suggests optionally removing “Reference” from the title. | Treat this as a low-priority editorial option. Retain the existing title if it matches the approved institutional record. |
| Repetition and terminology | Important caveats recur across chapters. The main paragraphs already use LLM-assisted and operator-hosted consistently. | Consolidate repeated explanations in scope, validity and conclusion sections, while retaining short qualifications beside standalone numerical claims. Do not mechanically alter grammatically correct phrases such as “targets a single host.” |
| References | There are 51 reference entries. The sampled documentation references already use consistent retrieval-date patterns. | Audit APA/institutional style, in-text matching, titles, italics and DOI/URL accuracy. Different formats for papers, changing documentation and legal sources are not automatically errors. Live links were not checked in this assessment. |
| Figures, captions and navigation | The inspected abstract, requirements, architecture, results, recommendations and Appendix F pages have no obvious clipping. Architecture labels remain relatively small. | Check diagrams at print size. After revision, refresh contents, lists and cross-references, then render and inspect the complete final document. This assessment is not a new full pagination sign-off. |

## Proposed RQ4 structure

Use the review's conceptual split without changing the study or inventing additional objectives:

- **RQ4a:** Which implemented behaviours are supported by automated software verification?
- **RQ4b:** What does the frozen qwen2.5:3b incident and RAG/no-RAG benchmark establish about severity agreement, signature stability and runbook retrieval?
- **RQ4c:** What does the retained SUS study indicate about perceived usability within the participating convenience sample?

Update Section 1.3.2, Table 3.1, the RO5 discussion in Table 5.12 and Section 6.2.1 together. Qualitative practitioner reports and threats to validity can remain supporting evidence across these answers.

## Strengthen the risk interpretation without changing the benchmark

The retained [incident score file](C:/Users/adebo/PROJECTS/infraguad_ai/evaluation/results/qwen2.5-3b-v1/incident_objective_scores.csv) reproduces the manuscript's confusion matrix and 29/72 exact matches.

The review's 33.3% high recall is **exact-class recall**, not the proportion of high cases that remained urgent. Of 24 high-labelled responses, eight were predicted high, ten critical and six warning. Thus, ten errors were upward escalations, while six were under-calls.

| Derived measure from the existing runs | Result |
|---|---|
| Exact high-class recall | 8/24 = 33.3% |
| High-labelled responses predicted warning | 6/24 = 25.0% |
| Combined high/critical-labelled responses still predicted high or critical | 24/30 = 80.0% |
| Combined high/critical-labelled responses predicted below high | 6/30 = 20.0% |

These are descriptive calculations from the existing researcher-labelled runs, not new experimental evidence. All six under-calls came from C15 and C17, each repeated three times. No critical-labelled response was under-called. The observations must not be described as six independent production incidents or generalised to the subsequently hardened implementation.

A useful discussion addition would explain that the acknowledgement safeguard operates on the **predicted verdict severity**. The current [suppression function](C:/Users/adebo/PROJECTS/infraguad_ai/api/store.py:70) permits masking acknowledged `ok` or `warning` verdicts, and the [acknowledgement route](C:/Users/adebo/PROJECTS/infraguad_ai/api/main.py:337) rejects verdicts labelled `high` or `critical`. Those rules cannot by themselves identify a serious real condition that the model has labelled warning. This is an inference from the code's decision boundary, not an observed suppression event in the benchmark.

## Resolve the practitioner wording precisely

The current file inspection establishes three separate facts:

1. The supplied DevOps and SRE report files are retained unchanged, and their hashes match the manuscript's recorded hashes. Their presence and report-level claims are distinct from availability of original item-level ratings.
2. The four public incident/RAG A/B worksheet CSVs each contain 72 rows but no populated human score or note cells. This limits recomputation from the inspected package. It does not prove that private examiner records do not exist or that no human review occurred.
3. The separate development files `devops_scores.json` and `sre_scores.json` contain explicit AI-simulated labels, and their hashes match the candidate files named in Appendix F. That finding applies to those files; it does not classify every practitioner report or examiner submission.

There is also a wording inconsistency to resolve: [summary.json](C:/Users/adebo/PROJECTS/infraguad_ai/evaluation/results/qwen2.5-3b-v1/summary.json:29) sets the human-scoring completion flags to true while separately recording that completed public item-level sheets are absent. The [practitioner README](C:/Users/adebo/PROJECTS/infraguad_ai/evaluation/practitioner_confirmation/README.md:27) reports confidential records outside the public repository. The manuscript should consistently distinguish researcher-reported completion, retained reports, available raw ratings, and independently recomputable findings.

Suggested direction for the revised wording:

> Two researcher-supplied DevOps and SRE practitioner reports are retained as exploratory report-level evidence. Completed original item-level ratings are not present in the inspected public package, so its aggregate assessor statistics cannot be independently recomputed from that package. Separately retained development scores explicitly labelled AI-simulated are excluded from human findings.

Do not reconstruct ratings from aggregate means or kappas. If original examiner records are verified separately, describe their actual provenance and scope. The review places stronger independent expert assessment in future work; it does not instruct the author to publish confidential identities or treat every report as simulated.

## Suggested coverage clarification

Replace the opening recommendation in Section 6.4.2 with wording such as:

> Maintain 100% line coverage for the selected modules that reached that level, and progressively improve overall source-scoped coverage beyond the recorded 89%. Retain regression checks and extend verification through controlled integration tests.

Keep the existing module list nearby. Retain the local working-tree qualification, and distinguish the 29 August verification from the 2 September repeat result using their retained records.

## Recommended revision order

1. Reconcile evidence scope, provenance wording and test chronology. Preserve the frozen benchmark and source records.
2. Split RQ4 and synchronise its alignment table and conclusion answers.
3. Complete requirement acceptance criteria and add the thematic literature synthesis.
4. Refine the label-policy, severity-risk and signature-identity discussion using the existing results.
5. Tighten the abstract and repeated caveats; audit references, terminology, models and counts.
6. Save a separate revised manuscript, update navigation and visually check the complete render. Prepare a response matrix giving each review item, disposition and exact revised section.

Larger expert panels, independently adjudicated labels, new human answer-quality scoring, cross-model comparisons, field trials, workload studies and adversarial security experiments should remain clearly specified future work unless separately required by the supervisor. The review's section 16 explicitly presents independent expert labelling as a stronger subsequent study, while sections 32–35 frame the present acceptance conditions around corrections and methodological clarity.
