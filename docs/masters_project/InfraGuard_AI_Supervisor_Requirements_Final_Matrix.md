# InfraGuard AI Supervisor Requirements — Final Compliance Matrix

**Audit date:** 28 August 2026  
**Audited manuscript:** `InfraGuard_AI_Masters_Project_DEFENCE_READY_REVISED.docx`  
**Audited presentation:** `InfraGuard_AI_Masters_Project_DEFENCE_PRESENTATION.pptx`  
**Human evidence:** two operations practitioners completed the exploratory benchmark scoring; 11 people consented to the separate SUS study and 10 complete responses were analysed without imputing the incomplete response.

## Overall conclusion

The supervisor's academic, methodological, infrastructure-security, test-coverage, editorial, and presentation requirements are addressed in the current defence artefacts. The claims remain deliberately bounded: software verification is not field diagnostic efficacy; the two-practitioner assessment and ten-response SUS result are small-sample evidence; and production still requires externally supplied TLS termination, managed secrets, least-privilege identities, recovery controls, and independent security verification.

## Requirement-by-requirement audit

| Domain | Supervisor requirement | Current verified treatment | Status |
|---|---|---|---|
| Research contribution | Partition the research void into knowledge, design/technology, engineering, and empirical domains. | Section 1.2.1 states all four gaps separately and links them to the study questions and evidence. | Met |
| Research contribution | Elevate fingerprint acknowledgement as the primary design contribution. | Sections 2.4, 3.4.5, and 6.3.2 define condition-and-ruleset acknowledgement using the condition signature, prompt version, and model, with expiry and severity safeguards. | Met |
| Theory | Replace generic summaries with scholarship on automation bias, human collaboration, alert fatigue, and trustworthy systems; add 10–20 strong references. | Section 2.1.7 synthesises these theories. The final list contains 44 references, a net addition of 14 over the reviewed version, with all references cited in text. | Met |
| Empirical boundary | State that artefact verification does not prove real-world diagnostic efficacy. | Chapters 4–6 distinguish controlled software/benchmark evidence from field reliability, workload, production safety, and population-level usability. | Met |
| Severity analysis | Analyse the 40.3% result deeply and use “exact severity accuracy.” | Sections 5.4.2.2 and 5.6.1 report 40.3% exact severity accuracy, macro-F1 0.383, warning recall 0%, high recall 33.3%, six high-severity undercalls, critical recall 100%, and critical precision 27.3%. | Met |
| Methodology | Justify SUS and connect the two human studies without conflating them. | Sections 3.1.6–3.1.7 explain why SUS measures perceived usability and separate A1/A2 benchmark scoring from P-series SUS respondents. | Met |
| Methodology | Discuss the two-rater constraint and signature-instability circularity. | Sections 5.6.2.1–5.6.2.2 state the small-rater limitation and the risk of using model-derived signatures to identify recurrence; only 10 of 24 scenarios had one stable signature. | Met |
| Infrastructure | Remove world-open development ingress. | Terraform creates no ingress by default. Port 443 is opt-in and source-gated, port 80 is optional redirect-only, management ports require trusted ranges, and Docker Compose binds the API to loopback. `terraform validate` passes. | Met |
| Infrastructure | Make production warnings prominent. | README requires HTTPS ingress, private telemetry/admin binding, managed secrets, least privilege, secure cookies, and independent verification, while stating that the repository does not provision TLS or managed-secret integration. | Met |
| Tests | Cover the LangChain agent and scheduled entry point. | The final run has 148 passing tests, 0 failures, 87% overall coverage; both targeted modules are at 100%. | Met |
| Tests | Cover Docker API/events and ChromaDB vector-store paths. | The Docker API collector, Docker event collector, and ChromaDB vector store are each at 100% line coverage in the final controlled run. | Met |
| Editorial | Standardise accuracy/suppression terminology. | “Exact severity accuracy” is used for classification. Acknowledgement/suppression is defined as masking the default dashboard view while inference and storage continue. | Met |
| Editorial | Audit captions, numbering, citations, DOI, and institutional authors. | The 93-page render contains 15 figure captions and 31 table captions; 44 references are cited; 215 navigation anchors resolve; DOI/URL and organisational-author forms were normalised. | Met |
| Presentation | Add Literature Review, Timeline and Resources, and APA References slides. | The 15-slide deck contains dedicated slides with those literal labels, uses the supplied sample's visual system, and includes source notes on every slide. | Met |

## Final verification record

| Check | Result |
|---|---:|
| Automated tests | 148 passed; 0 failed |
| Overall line coverage | 87% across 1,516 statements; 201 missed |
| Supervisor-targeted modules | 5 of 5 at 100% |
| Terraform formatting and validation | Passed |
| Manuscript pages visually reviewed | 93 |
| Manuscript references | 44; all cited |
| Figure and table captions | 15 figures; 31 tables |
| Resolved manuscript navigation anchors | 215 |
| Presentation slides visually reviewed | 15 |
| Presentation source-note sections | 15 of 15 |

## Human-study evidence boundary

The two benchmark assessors use A-series codes and the separate SUS respondents use P-series codes. The benchmark scoring supports exploratory human interpretation of frozen outputs. The SUS results—mean 79.25, median 83.75, sample standard deviation 18.18, and range 40.0–97.5—support favourable perceived usability only within the evaluated group. Neither study establishes population-level diagnostic correctness, workload reduction, task performance, field reliability, or production effectiveness.

## Residual limitations

- External providers, Docker/socket behaviour, and vector-store dependencies are mocked in the strengthened test suite.
- The 40.3% exact severity result is unsuitable for unattended triage.
- Two practitioner assessors and ten complete SUS responses are not representative samples.
- TLS termination, managed-secret integration, least-privilege service identities, recovery testing, and production security review remain deployment duties.
