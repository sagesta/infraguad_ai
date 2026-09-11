# InfraGuard AI Professor-Review Revision Matrix

> **Historical record — superseded on 27 August 2026.** This matrix documents
> an earlier revision stage when the controlled benchmark and human studies had
> not yet been completed. It must not be used to describe the current project
> or included as current submission evidence. Use
> `InfraGuard_AI_Final_Supervisor_Compliance_Review.md` and
> `InfraGuard_AI_Supervisor_Requirements_Final_Matrix.md` instead.

## Document control

- Review source: `Review - InfraGuard_AI_Samuel_adebodun.pdf`
- Preserved manuscript: `InfraGuard_AI_Masters_Project_REFINED_APA7_SUBMISSION_FINAL.docx`
- Revised manuscript: `InfraGuard_AI_Masters_Project_PROFESSOR_REVIEW_REVISED.docx`
- Revision date shown in the manuscript: August 2026
- Evidence rule: no benchmark, practitioner, latency, token, cost, or usability result has been invented. Where evidence does not yet exist, the revised manuscript identifies the protocol as unexecuted and narrows the claim.

## Response to the review

| Professor's concern | Revision made | Location in revised manuscript | Status and evidence boundary |
|---|---|---|---|
| The title could imply that inference is fully self-hosted even when a cloud model is selected. | Retitled the work as an **operator-hosted LLM-assisted** observability and incident-triage agent. The abstract now states which assets remain under operator control and when prompts leave the host. | Title page; Abstract; Sections 3.3 and 4.3.7 | Completed. The title now matches the implemented deployment boundary. |
| The May 2026 title-page date conflicted with results recorded on 16 August 2026. | Updated the submission/revision date to **August 2026**. | Title page | Completed. |
| Explicit research questions were missing. | Added five research questions covering bounded telemetry context, operator-hosted/provider-independent architecture, acknowledgement behaviour, evidence sufficiency, and security/data-governance constraints. | Section 1.3.2, displayed page 2 | Completed. |
| The objectives read mainly as build objectives rather than a research lifecycle. | Reframed the objectives as requirements analysis, design/implementation, RAG assistance, human oversight, and evidence-bounded evaluation. | Section 1.3.3, displayed page 3 | Completed. |
| The chain from problem to questions, methods, evidence, and conclusions was not explicit. | Added a research-question/objective/method/evidence/current-answer alignment table. | Table 3.4, displayed page 19 | Completed. Unresolved effectiveness questions are marked as unresolved rather than treated as achieved. |
| The literature review lacked a formal conceptual framework. | Added a conceptual explanation and diagram connecting telemetry, bounded context, LLM reasoning, evidence grounding, structured verdicts, operator oversight, response, and operational outcome. | Section 2.1.7 and Figure 2.1, displayed page 7 | Completed. |
| Academic gaps and engineering/product gaps were insufficiently distinguished. | Reworked the gap discussion to distinguish knowledge/evaluation gaps from deployability and implementation gaps, and elevated the condition-and-ruleset acknowledgement mechanism as the central design contribution. | Section 2.4; Sections 6.3.1–6.3.3 | Completed. |
| Design science was appropriate but not formalised as research logic. | Added an explicit design-science mapping from problem relevance through artefact, design principles, demonstration, evaluation, contribution, and communication. | Section 3.1.5 and Table 3.5, displayed page 19 | Completed. The evaluation cell is qualified by the evidence actually available. |
| Research-question-to-method alignment was missing. | Linked every research question to its objective, method, evidence source, and present answer. | Section 3.1.4 and Table 3.4 | Completed. |
| Security and data-governance requirements needed stronger specification. | Added security/data-governance non-functional requirements, a demonstration-versus-production security table, and an operational data-governance discussion. | Table 3.2; Section 4.3.6 and Table 4.3; Section 4.3.7 | Completed as requirements and limitations; no production-security or legal-compliance certification is claimed. |
| Nigerian data-protection implications were too descriptive. | Expanded the discussion of personal or sensitive data in telemetry, IP addresses, lawful purpose/basis, retention, processor terms, DPIA triggers, and cross-border cloud-model transfers. | Section 4.3.7, displayed page 43 | Completed at project-governance level. Organisation-specific legal assessment remains necessary before deployment. |
| Chapter Four described implementation choices without enough comparative justification. | Added alternatives and trade-offs for SQLite, ChromaDB/local ONNX embeddings, retrieval depth, two-process deployment, fingerprint construction, and deterministic threat detection. | Section 3.5.4 and Table 3.6, displayed page 33 | Completed. |
| The acknowledgement mechanism's real contribution and limitation needed stronger emphasis. | Elevated the fingerprint, prompt-version/model binding, expiry, severity safeguard, and operator-control pattern as a contribution. Repeatedly states that acknowledgement reduces repeated **display**, not model calls, cost, latency, or proven alert fatigue. | Sections 3.4.5, 5.3, 6.2, and 6.3.2 | Completed. |
| The manuscript sometimes implied operational effectiveness when only implementation behaviour had been verified. | Recast the abstract, Chapter Five, conclusion, and contribution language around functional verification, integration feasibility, and bounded current evidence. | Abstract; Chapter Five introduction; Sections 5.6, 6.1–6.3 | Completed. Claims of diagnostic accuracy, workload reduction, cost reduction, production effectiveness, and usability are explicitly excluded. |
| Sixty-six per cent coverage should not be treated as uniform validation. | Added high-confidence, partially verified, and largely unverified coverage classifications, including the low-coverage LangChain, vector-store, Docker, and scheduled-entry paths. | Section 5.2.1, displayed page 47 | Completed. These classes describe test evidence, not operational correctness. |
| Provider/model terminology was inconsistent. | Standardised references to the Gemini Developer API, Anthropic, OpenAI-compatible endpoints, and optional locally hosted Ollama. Distinguished provider interface, default configured model, and the model actually used in the pilot. | Abstract; Sections 3.3, 4.2.2–4.2.4; Table 5.4 | Completed. |
| The three-question live pilot lacked a clear configuration record. | Added a live pilot configuration table recording date, corpus, questions, agent state, provider interface, model used, default model, embedding model, retrieval depth, and evaluation boundary. | Table 5.4, displayed page 49 | Completed for reproducibility of the reported pilot. No baseline, latency, cost, or independent accuracy result is claimed. |
| A controlled incident benchmark was needed. | Added a fixed, versionable protocol with 24 controlled scenarios spanning healthy, degraded, failure, security, ambiguous, missing-telemetry, and recurring-condition cases. Added frozen gold severity and expected root-cause/action criteria. | Section 5.4.2; Appendix E.1–E.3, displayed pages 66–67 | **Protocol completed; experiment not executed.** No accuracy, false-positive, false-negative, latency, token, or cost result is reported. |
| Diagnostic scoring needed severity, root cause, action, grounding, output-validity, and signature measures. | Added per-response scoring rules, primary metrics, false-positive/false-negative definitions, repeated-run requirements, independent assessment, and assessor-agreement reporting. | Appendix E.3 | **Protocol completed; scores outstanding.** |
| RAG needed a labelled question set and RAG-versus-no-RAG baseline. | Added 12 labelled operational questions with frozen relevant runbooks, top-four retrieval criteria, grounding/relevance scoring, and matched RAG/no-RAG runs. | Appendix E.4, displayed page 68 | **Protocol completed; comparison not executed.** |
| The proposed practitioner evaluation had not been performed. | Renamed the section to make non-completion explicit; retained the proposed task script and SUS instrument; stated that ethics approval and participant consent are required. | Section 5.4.3; Appendix D | **Outstanding empirical work.** No SUS score or practitioner-usability conclusion is reported. |
| Figure 5.3 could be mistaken for completed evaluation evidence. | Renamed it **Proposed Five-Case Practitioner Evaluation Workflow** and placed it beside the explicit non-execution statement. | Figure 5.3, displayed page 50 | Completed. |
| The conclusion should answer each research question individually. | Added a bounded answer to RQ1–RQ5 and distinguished achieved implementation claims from unresolved empirical questions. | Section 6.2.1, displayed page 53 | Completed. |
| Demonstration security and production security needed a prominent distinction. | Added a three-column posture table covering ingress, telemetry ports, secrets, browser policy, audit records, and cloud-model data paths. | Table 4.3, displayed page 43 | Completed as a documented boundary. Production hardening remains future work. |
| TOC, list entries, captions, page numbers, and new sections needed consistent navigation. | Updated the TOC, list of figures, and list of tables; added dotted leaders, bookmarks, hyperlinks, caption navigation, and corrected final page numbers. | Front matter | Completed and verified: 198 navigation entries, 226 hyperlinks, 365 bookmarks, zero page mismatches, and zero broken internal links. |
| A final APA 7 and reference-list audit was recommended. | Preserved the existing citations and reference list while keeping new legal/governance claims within the already cited Nigeria Data Protection Act source. | References and Section 4.3.7 | Partially addressed. A final institutional APA 7 line-by-line audit of every entry remains advisable before submission. |

## Controlled evaluation package now defined

The revised Appendix E supplies the research design that was missing from the original evaluation layer:

- 24 fixed incident scenarios with frozen inputs and gold expectations;
- severity labels and operational definitions;
- independent scoring for severity, root cause, recommended action, evidence grounding, schema validity, and signature behaviour;
- false-positive and false-negative definitions;
- three repeated runs per scenario/provider/model configuration;
- latency, token-usage, and provider-reported cost capture;
- 12 labelled runbook questions under matched RAG and no-RAG conditions;
- retrieval-success, answer-correctness, and grounding measures;
- assessor blinding, raw-output retention, versioning, and reporting requirements.

This package is a protocol, not evidence that the system is diagnostically effective.

## Work that still requires real data

Before the thesis can make stronger effectiveness claims, the following must be completed and reported:

1. Execute all Appendix E incident scenarios with fixed provider/model versions and retain raw and parsed outputs.
2. Have independent assessors score the anonymised outputs and report agreement where sample size permits.
3. Execute the labelled RAG and no-RAG comparison, including repeated trials and retrieval-success reporting.
4. Record measured latency, provider token counts, and provider-reported cost from the same executions.
5. Obtain the required university approval and informed consent before administering the Appendix D tasks and SUS instrument to practitioners.
6. Conduct a longer field study before claiming reduced operator workload, reduced alert fatigue, improved response time, production security, or scalability.

## Final quality checks

- The original manuscript remains separate and untouched.
- The revised DOCX package passes an integrity check.
- The final PDF render contains 81 pages, all visually inspected.
- All 14 original inline figures remain present.
- The document retains all 340 original bookmarks and adds 25 for the new material.
- Static navigation page numbers match the final render with zero mismatches.
- The benchmark and practitioner-study non-completion statements are present in both the main text and appendices.
