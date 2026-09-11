# InfraGuard AI Supervisor Compliance Review — Historical 28 August Snapshot

> **HISTORICAL / SUPERSEDED:** This file records the state of the project and
> its internal compliance review on 28 August 2026. It is not the current
> submission decision and must not be used as evidence of supervisor acceptance
> or production validation. The current manuscript is
> `InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.docx`.
> All 148-test, 87%-coverage, artefact-hash, page-count, reference-count, and
> package statements below apply only to the preserved 28 August snapshot.

**Review date:** 28 August 2026

**Historical decision recorded on 28 August 2026:** **PASS — ready for defence,
subject only to the normal student submission actions listed below.** This
historical wording has been retained for provenance; it is not a current
acceptance claim.

## Artefacts that were authoritative for this historical snapshot

| Artefact | SHA-256 |
|---|---|
| `InfraGuard_AI_Masters_Project_DEFENCE_READY_REVISED.docx` | `5A67093C9BB6EBE9E5E216346AC341AC02E33DFA8A61A1B340F222485CDA0BB4` |
| `InfraGuard_AI_Masters_Project_DEFENCE_PRESENTATION.pptx` | `0DD9E8746DD4565F60B2983E9FE613E234DE8158F81B8F0140E7FA50A5887CD8` |
| `submission/InfraGuard_AI_Source_Code_DEFENCE_READY.zip` | `378C880A0CD4B735B07168FD6EB27493F645AE91DECCC7506036185BE229F182` |

## Supervisor-review compliance

| Domain | Required remediation | Verified final treatment | Decision |
|---|---|---|---|
| Research gap and contribution | Separate the knowledge, design/technology, engineering, and empirical gaps; make fingerprint acknowledgement the principal design contribution. | Section 1.2.1 distinguishes the four gaps. Chapters 2, 3, 4, and 6 position the condition-and-ruleset fingerprint acknowledgement, including expiry and severity safeguards, as the principal design contribution. | Met |
| Theoretical literature | Reduce generic technology description; address automation bias, human collaboration and control, alert fatigue, and trustworthy systems; add 10–20 strong sources. | Section 2.1.7 synthesises the required human-factors and trust literature. The final reference list contains 44 cited works, a net addition of 14 over the reviewed version. | Met |
| Empirical boundary | State that artefact verification does not establish field diagnostic efficacy. | Chapters 4–6 consistently separate controlled software and benchmark verification from live reliability, workload, production safety, and population-level diagnostic effectiveness. | Met |
| Severity result | Analyse the 40.3% result and use the term “exact severity accuracy.” | Sections 5.4.2.2 and 5.6.1 report 40.3% exact severity accuracy, macro-F1 0.383, warning recall 0%, high recall 33.3%, six high-severity undercalls, critical recall 100%, and critical precision 27.3%. The manuscript rejects unattended triage for the evaluated configuration. | Met |
| Methodology | Justify SUS, connect but distinguish the two human studies, and discuss the two-rater and signature-circularity constraints. | Sections 3.1.6–3.1.7 explain the SUS choice and separate A-series benchmark assessors from P-series SUS respondents. Sections 5.6.2.1–5.6.2.2 address the small-rater design and circularity risk caused by model-derived signature instability. | Met |
| Infrastructure security | Remove world-open ingress and elevate production safeguards. | Terraform creates no ingress by default; HTTPS is opt-in and CIDR-gated; port 80 is redirect-only; management ports require trusted ranges; the application API is loopback-bound in Docker Compose. The README explicitly requires HTTPS, private telemetry and administration, managed secrets, least privilege, secure cookies, recovery controls, and independent production-security verification. | Met |
| Test coverage | Cover the LangChain multi-tool path, scheduled entry point, Docker API/events collectors, and ChromaDB vector store. | The final run has 148 passing tests, 0 failures, and 87% overall line coverage. All five supervisor-targeted modules reached 100% line coverage in the controlled suite. | Met |
| Editorial quality | Standardise terminology, explain suppression correctly, and reconcile captions, numbering, citations, DOIs, and institutional authors. | “Exact severity accuracy” is used for classification performance. Acknowledgement/suppression is defined as default-view masking while inference and storage continue. The rendered manuscript contains 15 figure captions, 31 table captions, 44 cited references, and 215 resolved navigation anchors. | Met |
| Defence presentation | Follow the supplied sample and add Literature Review, Timeline and Resources, and APA References slides. | The 15-slide deck follows the supplied Miva/MIT visual system, contains the three required dedicated slides, and includes a manuscript/source note on every slide. Its visible selected-reference slide now foregrounds four current sources from 2023–2025 and retains only Hevner et al. (2004) as an explicitly foundational Design Science source. | Met |

## Historical verification record

| Check | Final result |
|---|---:|
| Automated tests | 148 passed; 0 failed; 23 dependency deprecation warnings |
| Overall line coverage | 87% across 1,516 statements; 201 missed |
| Supervisor-targeted modules | 5 of 5 at 100% |
| Clean extracted source archive | Reproduced 148 passed, 23 warnings, 87% across 1,516 statements with 201 missed; no private `.env` present |
| Terraform configuration | Formatted and validated successfully |
| Manuscript visual review | All 93 pages reviewed |
| References | 44; all cited in text |
| Figures and tables | 15 figure captions; 31 table captions |
| Navigation | 215 anchors resolved |
| Presentation visual review | All 15 slides reviewed |
| Presentation source notes | 15 of 15 slides; current AIOps, RCA, RAG evaluation, and governance scholarship added where relevant |
| Source archive | 95 current files; forbidden-entry scan returned 0 |

## Historical independent professor-level second-pass audit

The second-pass audit checked the final manuscript, presentation, test and
coverage evidence, Terraform safeguards, evidence provenance, source package,
and the supervisor's requirement matrix as one submission. First-pass findings
were resolved: three manuscript statements were corrected for precision; slide
titles and section-source notes were reconciled; evidence files were labelled
according to their verified status; historical rebuild sources were guarded or
marked as superseded; and the clean source archive was rebuilt from the current
submission list.

The final academic claims now tally with the evidence and the supervisor's
requested changes. No defence-blocking inconsistency remains.

## Human-evidence provenance boundary

The public repository contains the unchanged role-level practitioner reports
and their hashes, but it does not contain a completed public item-level scoring
sheet. The public aggregate practitioner result therefore cannot be
independently recomputed from repository files alone. The original submissions
and confidential identity mapping are researcher-reported as retained outside
the public repository. This is disclosed as a provenance and reproducibility
limitation. No missing item-level values were inferred, recreated, or imputed.

The two-practitioner benchmark and the separate SUS study are not conflated.
The 10 complete SUS responses support only descriptive perceived-usability
findings in the evaluated group; the incomplete eleventh response was not
imputed.

## Limitations to state during the defence

- The 40.3% exact severity result does not support unattended triage.
- Two practitioner assessors and 10 complete SUS responses are exploratory,
  small-sample evidence rather than population-level proof.
- External providers, Docker/socket behaviour, and vector-store dependencies
  are mocked in the strengthened test suite; this does not prove live or field
  reliability.
- TLS termination, managed-secret integration, least-privilege cloud identity,
  recovery testing, and production security review remain deployment duties.
- The test run reports 23 third-party deprecation warnings; they do not affect
  the passing result but should be monitored during dependency maintenance.

## Historical defence-package decision

Include the authoritative manuscript and presentation above, this compliance
review, and the 95-file source archive only if source submission is required.
Exclude earlier document and slide versions, historical generation sources,
legacy non-evidential assessment binaries, runtime artefacts, local databases,
logs, caches, credentials, and environment files.

Before upload, the student must obtain required signatures, confirm the portal's
filename and format rules, and open the final DOCX and PPTX on the actual defence
computer to confirm fonts, notes, and links.
