# InfraGuard AI final submission audit

## 1. FINAL VERDICT

**REQUIRES SIGNIFICANT REVISION**

The research is defensible as a bounded design-science reference implementation, but the current submission still needs two significant corrections: explain the historical C23 severity-policy exception and complete the factual research-ethics disposition. Minor technical, reproducibility and citation corrections are listed separately. These concern interpretation and documentation, not a need to redesign the project. No new model experiment, field trial or larger usability sample is required to support the thesis's presently bounded contribution.

**Document examined:** `InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_8_SEPTEMBER_REVIEW.docx`, 107 physical pages, 36 tables, 16 figures, 51 references. SHA-256: `270fdbe0f4ce91dafc78ba50e3431e361fa57c6cd9bb0e478eec4e3c1c429391`. The document was not edited. All chapters and appendices were read; all 107 pages of its matching Word render were visually inspected across three reviewers; 202 contents/list navigation destinations and page numbers were checked. Printed body page numbers are used below; add 12 for physical pages. Front matter retains Roman numbering.

**Audit boundary:** judgments about the study use the supplied thesis, including its tables and code excerpts. Repository code, raw experimental files, private participant records and earlier reviews were not used to fill omissions. External primary-source checks were limited to citation accuracy and link verification. Where the thesis cannot establish a fact, the finding is explicitly “Not verifiable from the supplied document.” An unavailable external record is not automatically evidence that it does not exist.

The supplied checklist's C1–C4 configurations, forecasting, predictive rate limiting and .NET/YARP stack belong to another study. They are not requirements for InfraGuard. C01–C24 in this thesis are synthetic incident scenarios, not four experimental configurations.

## 2. EXECUTIVE SUMMARY

**Strongest aspects.** The research problem, five objectives, research questions, architecture, evaluation boundaries and conclusions form a coherent chain. The manuscript reports negative findings prominently: low agreement with its severity policy and unstable model-generated signatures. It distinguishes current software verification from the frozen v1 benchmark, retrieval from answer quality, perceived usability from task effectiveness, and implemented application controls from production assurance. These are substantial strengths and are **RESOLVED / ACCEPTABLE**.

**Genuine weaknesses.** The historical C23 label conflicts with the stated general severity policy and current acknowledgement semantics. The ethics section discloses facts it cannot establish but does not yet supply an institutional disposition or a complete brief procedural account. Reproduction records give relative file paths without identifying an accessible frozen source/evidence deposit. Several small statements also disagree with their accompanying tables or appendices.

**Central contribution.** Supported as conceptual/prescriptive, architectural, engineering and configuration-specific empirical work. No new model-training algorithm, universal novelty, superior diagnosis, validated workload reduction or production security is demonstrated or required by the bounded aim.

| Identity question | What the thesis actually says |
|---|---|
| Problem | Small teams must interpret fragmented telemetry; recurring findings, unsupported model output and data/action boundaries complicate triage (§§1.1–1.2). |
| Aim | Design, implement and verify an operator-hosted LLM-assisted triage artefact with structured verdicts, local runbooks, approved threat response and acknowledgement (§1.3.1). |
| Objectives | RO1 requirements; RO2 architecture/implementation; RO3 RAG assistance; RO4 acknowledgement/human control; RO5 bounded verification/evaluation (§1.3.3). |
| Questions | RQ1 telemetry representation; RQ2 architecture; RQ3 acknowledgement; RQ4a software verification; RQ4b model/retrieval evidence; RQ4c SUS; RQ5 governance/control status (§1.3.2). |
| Hypotheses | No formal confirmatory statistical hypotheses. Table 5.10 contains explicitly untested engineering hypotheses for future work. |
| Implemented | Scheduled agent, FastAPI/dashboard, SQLite, bounded provider paths, local Markdown/Chroma retrieval, acknowledgement, deterministic threat detection and approved CrowdSec path (Chapters 3–4). |
| Experimentally evaluated | Dated local software suite; frozen qwen2.5:3b v1 incident and RAG/no-RAG runs; deterministic presentation illustration; descriptive SUS. |
| Demonstrated within scope | Specified software paths, schema conformance, researcher-policy agreement, signature instability, source reachability and perceived usability in the sample. |
| Not demonstrated | Reliable diagnosis, current v2 model quality, causal RAG answer benefit, safe recommendations, reduced workload/fatigue/cost, cross-model equivalence, live security, production resilience or scale. |

## 3. SUBMISSION-BLOCKING ISSUES

**No submission-blocking issues identified.**

No A-level scientific invalidity or proved institutional violation is established by the supplied document. This does not certify institutional acceptance. Whether formal ethics approval/exemption and completed approval signatures are required at this submission stage is **Not verifiable from the supplied document**. The unresolved factual ethics account is classified B2, rather than inventing an institutional rule or alleging misconduct.

## 4. SIGNIFICANT REVISIONS

### B1 — Explain the historical C23 severity-policy exception

**Location/evidence:** Table E.2, C23 (p. 90), gives an unchanged acknowledged disk warning the expectation **“ok with the acknowledged signature”**. Table E.1 (p. 88) defines warning as existing degradation without immediate outage/data-loss risk. Appendix B.3 (p. 82) says **“Never reduce severity because an identifier is listed.”** Sections 3.4.5 and 4.2.2 describe current presentation masking rather than severity downgrading.

**Why it matters:** The document distinguishes v1 from v2 in general, but does not identify C23 as an exception to its stated telemetry-based policy. A reader could interpret its primary agreement score as uniform agreement with Table E.1, or mistakenly conclude that acknowledgement itself makes a warning healthy. This affects the central acknowledgement construct. It also affects the description “healthy false positives”: the five gold-ok cases include the acknowledged degradation case C23.

**Exact correction:** Preserve the frozen label, matrix and primary 29/72 result. Add a note at Table E.2 and cross-reference it in §5.4.2.2 and Table E.5:

> C23 retains the historical v1 expectation of ok for an acknowledged unchanged disk warning. This is an acknowledgement-conditioned exception to the telemetry-based severity definitions in Table E.1. It is not the current v2 rule, which retains telemetry-based severity and changes only eligible default presentation. The primary 29/72 agreement remains a result under the frozen v1 policy and is not validation of the current no-downgrade contract.

For the healthy-false-positive description, distinguish C01–C03/C21 (12 healthy or no-impact response runs) from C23 (three acknowledged-degradation runs). All gold-ok entries are predicted ok in Table 5.6, so there were zero escalations among those 12 healthy/no-impact runs; C23 should be described separately. Do not silently relabel C23 or replace the primary analysis.

An explicitly post hoc exclusion sensitivity is optional: removing C23's three correct-under-v1 responses yields **26/69 = 37.7%**. This is derived from the supplied case definitions and aggregate matrix, not from an independently reopened raw dataset. It must not be represented as a new primary result.

**Status after correction:** The history/current-design distinction becomes defensible without rerunning the benchmark; the limited-reliability conclusion remains unchanged.

### B2 — Complete the factual ethics and participant-record account

**Location/evidence:** §3.1.4 (p. 24) confirms researcher custody, 60-day retention and coded public results, but expressly states that formal approval/exemption, the full information/withdrawal procedure and detailed access/deletion arrangements are not established. §§3.1.3, 5.4.3 and Appendix D describe human participation.

**Why it matters:** Honest disclosure prevents a false approval claim, but does not resolve how the completed human study was authorised and handled. The required institutional route is **Not verifiable from the supplied document**. The absence of a public private-record file does not itself invalidate the study.

**Exact action:** Record the actual institutional disposition, if available: approval, exemption, confirmation that review was not required, or the truthful unresolved status and the institution's decision on use of the study. Add a short factual account of information/consent, withdrawal arrangements, who could access records, the event from which the 60 days runs, which records it covers and the intended deletion/anonymisation method. Use only confirmed facts. If something was not recorded, say so. Do not manufacture retrospective approval or claim deletion has happened.

Keep identity/contact evidence confidential. This correction requires a concise factual statement and any appropriate private verification, not publication of names, emails or consent forms. The 60-day research-record period remains separate from the default 30-day application-verdict retention.

**Status after correction:** Ready for institutional assessment of the human-evidence component. If a required process was not followed, the institution must determine the remedy; prose alone cannot supply an approval decision.

## 5. MINOR CORRECTIONS

### C5 detail — Make the frozen reproduction package locatable and qualify execution details

**Location/evidence:** §6.3 (pp. 71–72) calls the engineering contribution a reproducible reference implementation. Table E.5 (§E.7, pp. 92–93) gives `evaluation/benchmark_v1.json`, `evaluation/run_benchmark.py` and result-directory paths, with a specification hash and model digest. It does not identify a repository URL, archive/deposit or examiner-supplement access locator, or a specific retrievable v1 source snapshot/manifest location. It correctly warns that the current working tree differs from v1.

**Why it matters:** A relative path and checksum identify content once obtained; they do not tell another examiner where to obtain the historical source and evidence. Availability of a complete executable v1 package is **Not verifiable from the supplied document**. The dirty-working-tree limitation is already adequately disclosed and is not itself a new defect.

**Exact action:** Add one evidence-access statement naming an existing versioned archive, repository/ref, institutional deposit or supplied examiner supplement, its access arrangement, and the exact v1 manifest/source location. Identify the frozen specification, prompt, corpus, harness, response rows and analysis procedure within that package. Public release is not required; controlled examiner access is sufficient. Do not insert an invented commit or claim that the revised tree reproduces the historical run. If the complete v1 source was not retained, replace exact-rerun implications with the narrower statement that retained records permit inspection/recalculation, while an exact rerun is not established.

**Classification and status after correction:** C-level reporting clarification, consolidated with C5 below. The thesis already limits the local test receipt and makes no causal speed or exact-output replication claim. A precise access/settings statement or a narrower reproducibility description closes the gap; no new experiment is required. Where exact historical source recovery is unavailable, use the heading “Engineering contribution — inspectable reference implementation.”

| ID | Location | Current issue | Targeted correction |
|---|---|---|---|
| C1 | §2.4.6 p. 19; Appendix C p. 84 | Prose says runbooks mount in both API and agent; shown Compose mounts them only in API. Appendix C also calls the Docker socket optional while its shown agent mount is unconditional. | Say runbooks are mounted read-only in the API container. Distinguish optional monitoring from the shown socket mount, which remains present unless removed from the composition. |
| C2 | Table 4.2 p. 49; Appendix A pp. 79–80 | Combined `/login, /logout` GET/POST entry obscures GET-only logout; Appendix A omits the explicit `/api/config` entry and method/path for runbook indexing. | Separate GET/POST `/login` and GET `/logout`; add GET `/api/config` and POST `/api/runbooks/index` to Appendix A, using Table 4.2 as the document-internal reference. |
| C3 | §5.4.2.6/Table 5.10 p. 65; Appendix F.2 p. 94 | “Weakest scenarios” implies a ranking despite the explicit exclusion of ranked human findings. “Severity calibration” can be confused with probability calibration. | Use “candidate scenarios and questions highlighted in the role reports”; use “severity-policy alignment” for this theme. If P0–P2 priorities remain, identify them as proposed engineering priorities rather than measured assessor rankings. |
| C4 | §§3.1.3, 5.4.3 and Appendix D | “Anonymised” identifiers coexist with a retained confidential identity mapping. | Use “coded participant identifiers” or “de-identified public responses”; explain that the mapping remains separate. Incorporate into B2 without duplicating it as another significant finding. |
| C5 | Table 5.4 pp. 61–62; Tables 5.5/5.7 pp. 62–63; Appendix E.7 pp. 92–93 | Model/runtime details are given, but benchmark CPU/RAM/GPU, confirmed execution OS, request limits/timeouts, order/warm-up/reset state, latency boundary and percentile method are not specified. | Add only historically retained details; otherwise state they were not retained and limit timings to descriptive observations from that execution. Do not infer timeout censoring from silence or substitute today's machine details. No new performance experiment is required. |
| C6 | §2.1.5 p. 8 | Es et al. (2024) is attached to a four-part evaluation statement including actionable safety, although the cited RAGAs paper presents faithfulness, answer relevance and context relevance. | Separate the source's dimensions from this thesis's added correctness and operational-safety criteria; use the replacement below. |
| C7 | Figure 3.3 p. 35 versus Figure 3.5 p. 38 | Figure 3.3 places fingerprint/storage before optional Docker diagnostics; Figure 3.5 places diagnostics before persistence. | Align to the documented historical implementation sequence, or explicitly label Figure 3.3 as a logical overview rather than execution order. The exact executed order is not verifiable from the supplied excerpts alone. |
| C8 | Table 3.7 p. 42 | “Deterministic context size” is attributed to retrieving four variable-length whole Markdown files. | Replace with “A fixed maximum of four retrieved documents limits source count; context length varies with document length.” No new top-k experiment is required. |
| C9 | Table 2.1 row 5 p. 13 | Reflexion is characterised as “Toy code/QA tasks,” omitting its sequential decision-making tasks. | Replace with “Benchmark decision-making, reasoning and coding tasks; no incident-triage field trial.” |

**C6 replacement:** “Es et al. (2024) distinguish faithfulness, answer relevance and context relevance in RAG evaluation. This study additionally treats answer correctness and actionable safety as separate operational criteria. Retrieval success alone establishes neither.” The source supports the separation but does not supply a validated actionable-safety measure. [RAGAs, §3](https://aclanthology.org/2024.eacl-demo.16.pdf).

C9 follows the tasks actually evaluated in the published source. [Reflexion, abstract and §4](https://proceedings.nips.cc/paper_files/paper/2023/file/1b44b878bb782e6954cd888628510e90-Paper-Conference.pdf).

No material clipping, overlap, missing glyphs, blank pages, orphan headings or broken contents/list links was found. Sparse chapter endings and contents-list continuation pages are not empty-page defects. No tracked changes or comment part remains.

## 6. OPTIONAL ENHANCEMENTS

These are **not submission blockers**: an abbreviations list if the institution prefers one; shorter repeated provenance passages; and a separately labelled C23 sensitivity calculation after the mandatory historical-policy clarification. A new independent label panel, larger SUS sample, cross-model study, field evaluation and live red-team assessment are already reasonable future work. They are not additional requirements for this bounded submission.

No institutional template was supplied. The original August title date and unsigned certification/approval lines should follow the actual submission stage; neither is automatically an academic defect. Certification already contains the originality declaration. Appendix F provides evidence provenance and is not an inappropriate reviewer-response appendix.

## 7. CROSS-CHAPTER CONSISTENCY MATRIX

| Topic | Cross-check | Status |
|---|---|---|
| Problem, aim, objectives | Chapter 1 → Tables 3.1/3.2 → Table 5.12 → §6.2.1 | RESOLVED / ACCEPTABLE: implementation and bounded evaluation are aligned. |
| Governance contribution | §1.2.2 → §§2.1.8/2.4 → §4.3 → §6.3/Table 6.1 | RESOLVED / ACCEPTABLE: prescriptive integration, not complete organisational or legal assurance. |
| Current acknowledgement | §§3.4.5/4.2.2 → §5.4.2.2 → §6.2.1 → B.2/B.3 | Current design is coherent; B1 corrects the unexplained historical C23 exception. |
| Predicted versus actual severity | §1.2.2/Table 3.5 → §5.4.2.2 → §6.3 | RESOLVED / ACCEPTABLE: misclassified serious warnings are not independently rescued by the safeguard. |
| v1 benchmark versus v2 implementation | §4.2.2 → §5.4.2 → Table 5.13 → §E.7 | RESOLVED / ACCEPTABLE apart from the specific C23 policy note. |
| Tests and source scope | Abstract → Table 5.1 → §§5.6/6.2.1 → Table E.5 | RESOLVED / ACCEPTABLE: 180 tests/89% apply to a dated local working tree. |
| RAG | §2.1.5 → §§3.4.7/4.2.3 → Tables 5.7/5.9 → §6.2.1 | Retrieval evidence is coherent; C6 clarifies citation scope. |
| SUS and qualitative role reports | §§3.1.3–3.1.4 → §§5.4.2–5.4.3 → Appendices D/F | Evidence streams remain separate; B2 resolves ethics facts. |
| Deployment | §§3.3.5/4.1/4.3 → Appendix C | Intended topology and live proof separated; C1/C2 fix documentation details. |
| Reproduction | §6.3 → Appendix E.7 | C5: identify evidence access and complete or qualify runtime/reproduction details. |
| Heartbeat diagram order | Figure 3.3 → Figure 3.5 | C7: reconcile the diagnostics/persistence sequence or distinguish logical overview from execution order. |
| Abstract and conclusion | Abstract → Chapter 5 → Chapter 6 | RESOLVED / ACCEPTABLE for reported numerical findings and scoped contribution; neither claims predictive or production superiority. |

**Requirements audit.** Table 3.5 traces all 15 functional and 14 non-functional requirements to a source, acceptance criterion and evidence class. Priorities/thresholds are engineering targets rather than statistical findings. The summary below classifies what the thesis supports; it does not claim a new execution of its tests.

| Requirement | Target / method described | Document-supported disposition |
|---|---|---|
| FR-01 | Configured telemetry per heartbeat; adapter fixtures | Verified in mocked/fixture scope. |
| FR-02 | Five-field verdict or visible failure; parser/orchestration tests | Verified software contract; not diagnostic correctness. |
| FR-03 | Four allowed severities; schema tests | Verified canonical values; not valid real-world classification. |
| FR-04 | Direct and multi-tool dispatch; mocked path tests | Verified dispatch, not equal model quality. |
| FR-05 | High/critical notification dispatch | Dispatch asserted; external receipt unverified. |
| FR-06 | SQLite persistence/pruning | Verified temporary-store behaviour. |
| FR-07 | Eligible fingerprint acknowledgement/masking | Verified matching behaviour; stable model identity not established. |
| FR-08 | Signature/version/model change and expiry | Verified deterministic changes; real condition recognition unverified. |
| FR-09 | High/critical visibility | Verified for predicted labels; serious under-calls remain possible. |
| FR-10 | Deterministic threat patterns/IPs | Inspected and fixture-tested; broad detection effectiveness unverified. |
| FR-11 | Approved current threat or dry run | Selection/control tests; live rollback unverified. |
| FR-12 | Whole Markdown indexing/local retrieval | Verified selected index paths and frozen retrieval. |
| FR-13 | Context-conditioned advisory answer/source titles | Interface/retrieval supported; correctness/safety unresolved. |
| FR-14 | Dashboard functions | Inspected plus API tests; complete browser acceptance unverified. |
| FR-15 | Boolean integration status without secrets | Inspection/test assertion supports target. |
| NFR-01 | Configurable interval and bounded context | Scheduler/prompt checks; multi-tool calls and total cost not bounded by one-call assumption. |
| NFR-02 | Configured evidence and untrusted-data boundaries | Construction verified; live injection resistance unverified. |
| NFR-03 | Blocking work dispatched to threads | Source/API evidence; concurrent responsiveness unmeasured. |
| NFR-04 | Signed session, 24-hour maximum | Authentication tests and inspection; not independent security assurance. |
| NFR-05 | 60 requests/minute; 5 login attempts/minute | Login limit tested/general middleware inspected; engineering settings. |
| NFR-06 | Escaping/headers | Selected paths checked; complete adversarial assurance absent. |
| NFR-07 | Structured local audit | Implemented record path; delivery completeness/tamper evidence unverified. |
| NFR-08 | Single-host Compose | Configuration inspected; production receipt not established. |
| NFR-09 | Dated test/coverage record | 180 passed, 89% in dated local snapshot; coverage not sole quality measure. |
| NFR-10 | Selected telemetry only | Selected construction paths verified; no complete DLP. |
| NFR-11 | Default 30-day verdict pruning | Store assertions support configurable policy. |
| NFR-12 | Deterministic fallback normalisation | Verified fallback only; frozen model signatures stable for 10/24 cases. |
| NFR-13 | Provider/model and prompt data boundary | Identifiable path; external handling/compliance unverified. |
| NFR-14 | HTTPS/private origin deployment posture | Specified/configuration-reviewed; effective production security unverified. |

No arbitrary statistical success threshold is used to declare the artefact effective. Top-four retrieval is explicitly an unoptimised engineering default. The 120-second heartbeat, rate limits, 24-hour sessions and 30-day verdict retention need not be experimentally optimised to be defensible configuration choices. The participant-record period is a different policy.

## 8. CLAIM → EVIDENCE AUDIT

| Major claim | Evidence in thesis | Judgment / defensible boundary |
|---|---|---|
| Implemented inspectable triage framework | Architecture, code excerpts, Tables 3.5/5.1/5.2 | Supported as reference implementation; C5 clarifies access. |
| 180 tests at 89% coverage | Table 5.1, dated 2 September snapshot | Supported as reported local receipt; clean-checkout reproduction not established. |
| 100% schema validity | 72/72 in Table 5.5 | Historical v1 output-form result only; not v2 live-model or accuracy proof. |
| 40.3% severity agreement | Table 5.6 diagonal 29/72 | Arithmetic supported; B1 qualifies heterogeneous frozen policy. |
| Acknowledgement masks recurring eligible rows | Tests and deterministic 30-cycle illustration | Supported conditionally on exact matching; no measured workload/cost benefit. |
| Serious verdicts remain visible | Predicted-severity rule and B.2 | Applies to verdicts labelled high/critical, not all actually serious conditions. |
| Model identity is insufficiently stable | 10/24 repeat-stable scenarios | Supported for frozen configuration; not universal model impossibility. |
| RAG retrieves relevant sources | 12/12 questions hit in top four | Frozen-corpus hit rate, not grounding, correctness or safe action. |
| Favourable usability | Ten SUS scores, mean 79.25, wide range 40–97.5 | Descriptive perception in convenience sample; no workload/task/role causality. |
| Human authority over supported action | Operator-mediated CrowdSec; no runbook execution | Implemented boundary, not evidence operators reliably reject wrong advice. |
| Local governance/data control | §4.3 local/cloud/ntfy boundaries | Application mechanisms only; no blanket sovereignty/security/compliance claim. |
| Qualitative practitioner concerns | Provenance-limited reports in Appendix F | Hypothesis generation only; C3 removes implied ranking. |

No major claim of predictive superiority, statistical significance, reliable unattended diagnosis, lower operating cost or cross-model equivalence is made. Do not invent such claims in a review.

## 9. HYPOTHESIS AUDIT

There are no H0/H1 hypotheses in this design-science study. Their absence is acceptable: the thesis asks design and descriptive evaluation questions. Normality testing, Welch/Mann–Whitney selection, p-values, inferential effect sizes and Bonferroni adjustment are therefore not missing mandatory analyses.

| Hypothesis or question class | Experiment/metric/result | Test, p-value, effect size | Outcome |
|---|---|---|---|
| Formal confirmatory hypotheses | None stated | Not applicable | No supported/rejected formal-hypothesis outcome to harmonise. |
| Reliable severity/identity, if inferred as expectations | Frozen agreement 40.3%, stable signatures 41.7% | Descriptive; no inferential test | Reliability not established; correctly acknowledged. |
| RAG improves correctness or safe action | Retrieval hit rate and runtime only; no adopted answer-quality ratings | Not applicable | Not testable from available adopted evidence; not claimed supported. |
| SUS indicates perceived usability | Mean79.25, n = 10 | Descriptive; no population/role test | Supported only within sample. |
| Table 5.10 proposed severity/sequence/security/diagnostic/identity/grounding improvements | Report-derived candidate engineering actions | No executed confirmatory test or p-value | Untested future hypotheses, not findings of effectiveness. |

Repeated runs are nested within 24 purposive scenarios; RAG generations are nested within 12 questions and condition. The manuscript recognises this and does not turn 72 outputs into 72 independent incidents. The small samples and absence of probability calibration are disclosed. Confidence intervals would not turn this purposive set into a production-population estimate and are not required for the descriptive claims.

## 10. EXPERIMENTAL CONFIGURATION AUDIT

| Configuration/evidence stream | Active | Inactive/not established | Unit and supported comparison |
|---|---|---|---|
| Current v2 software verification | Local application tests, mock upstream services, strict parser, acknowledgement/control paths | No new v2 model benchmark, clean-release or live-production proof | Dated software assertions only. |
| Frozen v1 incident benchmark | qwen2.5:3b, Ollama0.30.11, Q4_K_M, temperature0, fixed scenarios/prompt; three runs each | No multi-model comparator, operational rollout or human task experiment; full mode/state settings not supplied | 24 scenarios/72 nested outputs; agreement with frozen labels and signature behaviour. |
| Frozen RAG | Same model; local runbooks/embeddings; top-four context | No adopted completed answer-quality/safety ratings | 12 questions ×3 =36 generations. Source reachability and observed runtime. |
| Frozen no-RAG | Same model/questions; no retrieved source context | Retrieval and supplied-source traceability absent | 12 questions ×3 =36 generations. No-RAG comparator does not establish a causal answer-quality benefit. |
| 30-cycle acknowledgement illustration | Identical warning fingerprint; acknowledgement aftercycle 3 | No human workload or field observations; inference/storage continue | Deterministic display mechanism:27laterrows hidden under stated condition. |
| Convenience pilot | Three illustrative dashboard/runbook questions, DeepSeek-labelled route,20runbooks | Heartbeat intentionally stopped; raw answers/timings/baseline absent | Researcher-reported feasibility only. |
| SUS | Eleven consented submissions; ten complete questionnaires | No role inference, task timing, error or workload instrumentation | Participant is unit; descriptive scores only. |

C1–C4, route-gating ablations, forecasting, adaptive rate-limit ablations, prediction-versus-reactive effects and unmitigated load baselines are **not applicable**. InfraGuard's API request throttling is a security control, not a studied adaptive traffic-control mechanism.

RAG changes both evidence availability and prompt size. Execution order, warm-up/cache effects, generation ceilings and exact timing boundaries are not established in the thesis. Its medians and tails therefore describe recorded conditions; they do not isolate a general causal latency penalty. The thesis does not claim such a penalty or RAG superiority.

**Implemented versus reference architecture:** Docker Compose, Python/FastAPI, SQLite, LangGraph/provider adapters and local Chroma retrieval are the implementation described. Linux-VPS/Cloudflare ingress is an intended topology without a retained deployment receipt. Kubernetes appears in literature/product discussion; distributed tracing is expressly outside scope. Redis/PostgreSQL appear as incident/runbook subjects, not InfraGuard's own database implementation. Istio, Envoy, YARP, SQL Server, .NET, gRPC, trained anomaly detection, autoscaling, multi-region operation and autonomous code remediation are not experimentally implemented claims.

## 11. NUMERICAL CONSISTENCY AUDIT

**No material numerical inconsistencies identified.** B1 is a policy/denominator interpretation issue, not incorrect arithmetic in the published matrix.

| Quantity | Document arithmetic checked | Result |
|---|---|---|
| Incident observations | 24 ×3 | 72 |
| Gold class totals | 15+27+24+6 | 72 |
| Prediction totals | 27+6+17+22 | 72 |
| Exact agreement | (15+0+8+6)/72 | 40.2778% →40.3% |
| Macro precision/recall/F1 | Unweighted four-class averages from matrix | 0.324718/0.583333/0.383275 →0.325/0.583/0.383 |
| High-class recall | 8/24 | 33.3% |
| Combined urgent recall/under-call | 24/30 and 6/30 | 80.0% and 20.0% |
| Under-call cases | C15 and C17, each repeated 3 times | Six outputs from two scenario families |
| Signature stability | 10/24 | 41.7% |
| C20 exclusion sensitivity | 29/69 | 42.0%, explicitly post hoc |
| RAG counts | 12 questions ×3 ×2conditions | 72; 36 per condition |
| Retrieval hit rate | 12/12 | 100% |
| SUS complete-case proportion | 10/11 | 90.9% |
| SUS mean/median/sample SD | Table D.1's ten scores | 79.25/83.75/18.1831 →18.18 |
| SUS range | Table D.1 min/max | 40.0–97.5 |
| SUS role means | Five scores per role | 87.0 and71.5, descriptive only |
| SUS mean from item means | 2.5×[sum(odd means−1)+sum(5−even means)] | 79.25 |
| Coverage chronology | (statements−missed)/statements | 65.5827%,86.7414%,88.5196% →66%,87%,89% |
| Display illustration | 30 total − 3 before acknowledgement | 27 later repetitions; no saved model calls |

**Metrics that cannot be independently recalculated from this DOCX:** raw latency percentiles, token means, individual signature-match decisions and question-level retrieval ranks. The manuscript reports them and identifies external records, but does not embed the observations. Individual SUS item validity also requires the named workbook; the published participant-score and item-mean summaries are internally consistent. These limits are **Not verifiable from the supplied document** at raw-record level, not newly discovered numerical contradictions.

p50/p95 are local generation wall-clock summaries, not full incident-resolution or system-load latency. Timeout treatment, truncation and percentile estimator need C5's reporting clarification; no actual censoring defect is established. The US$0.00 value is explicitly metered API cost, with energy/hardware excluded. MAPE, MAE, WAPE, sMAPE, p99, transaction success, throughput and CPU-utilisation outcomes are not thesis metrics. CPU percentages in fixtures define scenario input, not measured system performance.

## 12. CITATION/REFERENCE AUDIT

All **51 reference-list entries** have corresponding citations in the prose or tables; no unmatched in-text author/year citation, uncited entry or duplicate reference was identified. The base is sufficient for the bounded contribution. No blanket request for more references is justified.

C6 and C9 are the targeted source-characterisation corrections: distinguish the cited RAGAs dimensions from this study's added operational correctness/safety criteria, and accurately describe Reflexion's evaluated tasks. There is no need to replace the whole literature review. The empirical AIOps comparison deliberately separates unlike tasks and does not rank unlike accuracy figures.

All **49 reference URLs** were attempted: 24 returned HTTP 200, 21 returned HTTP 403 and four returned HTTP 202. Among the HTTP 200 responses, two were browser-verification screens and one was a redirect shell. These responses are not proof of broken citations or of full source access. No 404/410 dead link was established. Reachability, bibliographic matching and support for a particular claim are different checks; an HTTP 200 alone does not certify the entire reference. A full source-by-source reconciliation and access-result ledger accompanies the audit's internal evidence. Primary-source checks corroborated the central comparative figures and the DSR/governance/human-reliance framing. Source access that remained blocked is recorded as unverified, not silently certified.

Reference style is broadly consistent author–date, with meaningful source identifiers. An institutional formatting mandate was not supplied. No citation-format issue was found that changes the central research conclusion.

<details>
<summary>All 51 reference entries and URL access attempts</summary>

Every entry below has a body or table citation. HTTP status records the initial access attempt, not verification of every attributed claim. A 403/202, verification page or redirect shell is unresolved access rather than an established dead link.

| Reference | Initial access result |
|---|---|
| [Ahmed (2023)](https://doi.org/10.1109/ICSE48619.2023.00149) | HTTP 202 |
| [Amershi (2019)](https://doi.org/10.1145/3290605.3300233) | HTTP unavailable |
| [Bangor (2008)](https://doi.org/10.1080/10447310802205776) | HTTP unavailable |
| Beyer (2016) | No URL supplied; book or book chapter identified bibliographically |
| [Bliss (1995)](https://doi.org/10.1080/00140139508925269) | HTTP unavailable |
| Brooke (1996) | No URL supplied; book or book chapter identified bibliographically |
| [Buçinca (2021)](https://doi.org/10.1145/3449287) | HTTP unavailable |
| [Central Bank of Nigeria (2024)](https://www.cbn.gov.ng/Out/2024/BSD/CBN%20Risk-Based%20Cybersecurity%20Framework%20for%20DMBs%20and%20PSBs_2024.pdf) | HTTP unavailable |
| [Chen (2025)](https://proceedings.mlsys.org/paper_files/paper/2025/hash/d1f9e4a9f109b6e8b75ed362736f22ec-Abstract-Conference.html) | HTTP 200 |
| [Chen (2024)](https://doi.org/10.1145/3627703.3629553) | HTTP unavailable |
| [Cvach (2012)](https://doi.org/10.2345/0899-8205-46.4.268) | HTTP unavailable |
| [Datadog (n.d.)](https://docs.datadoghq.com/bits_ai/bits_investigation/knowledge_sources/) | HTTP 200 |
| [Es (2024)](https://doi.org/10.18653/v1/2024.eacl-demo.16) | HTTP 200 |
| [Federal Republic of Nigeria (2023)](https://ndpc.gov.ng/download/nigeria-data-protection-act-2023) | HTTP 200 |
| [Gemini 2.5 Team (2025)](https://doi.org/10.48550/arXiv.2507.06261) | HTTP 200 |
| [Grafana Labs (n.d.)](https://grafana.com/docs/loki/latest/) | HTTP 200 |
| [Gregor (2013)](https://doi.org/10.25300/MISQ/2013/37.2.01) | HTTP unavailable |
| [Guo (2024)](https://openreview.net/forum?id=SZOQ9RKYJu) | HTTP 200 |
| [He (2017)](https://doi.org/10.1109/ICWS.2017.13) | HTTP 202 |
| [Hevner (2004)](https://doi.org/10.2307/25148625) | HTTP unavailable |
| [Hou (2024)](https://doi.org/10.1145/3695988) | HTTP unavailable |
| [International Organization for Standardization (2022)](https://www.iso.org/standard/27001) | HTTP unavailable |
| [Jacovi (2021)](https://doi.org/10.1145/3442188.3445923) | HTTP unavailable |
| [Jin (2023)](https://doi.org/10.1145/3611643.3613891) | HTTP unavailable |
| [K8sGPT (n.d.)](https://docs.k8sgpt.ai/getting-started/getting-started/) | HTTP 200 |
| [LangChain (n.d.)](https://docs.langchain.com/oss/python/langgraph/overview) | HTTP 200 |
| [Lee (2004)](https://doi.org/10.1518/hfes.46.1.50_30392) | HTTP unavailable |
| [Lewis (2020)](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) | HTTP 200 |
| [Mäntymäki (2022)](https://doi.org/10.1007/s43681-022-00143-x) | HTTP 200 |
| [Morley (2020)](https://doi.org/10.1007/s11948-019-00165-5) | HTTP 200 |
| [Mulligan (2018)](https://doi.org/10.15779/Z38QN5ZB5H) | HTTP 202 |
| [National Institute of Standards and Technology (2023)](https://doi.org/10.6028/NIST.AI.100-1) | HTTP 200 |
| [National Institute of Standards and Technology (2024)](https://doi.org/10.6028/NIST.AI.600-1) | HTTP 200 |
| [New Relic (n.d.)](https://docs.newrelic.com/docs/agentic-ai/new-relic-ai/) | HTTP 200 |
| [OpenAPI Initiative (2025)](https://spec.openapis.org/oas/v3.1.2.html) | HTTP 200 |
| [OWASP Foundation (2025)](https://owasp.org/Top10/) | HTTP 200 |
| [PagerDuty (n.d.)](https://support.pagerduty.com/main/docs/aiops) | HTTP 200 |
| [Parasuraman (2010)](https://doi.org/10.1177/0018720810376055) | HTTP unavailable |
| [Parasuraman (1997)](https://doi.org/10.1518/001872097778543886) | HTTP unavailable |
| [Parasuraman (2000)](https://doi.org/10.1109/3468.844354) | HTTP 202 |
| [Peffers (2007)](https://doi.org/10.2753/MIS0742-1222240302) | HTTP unavailable |
| [Prometheus Authors (n.d.)](https://prometheus.io/docs/instrumenting/exposition_formats/) | HTTP 200 |
| [Raji (2020)](https://doi.org/10.1145/3351095.3372873) | HTTP unavailable |
| [Roy (2024)](https://doi.org/10.1145/3663529.3663841) | HTTP unavailable |
| [Salah (2013)](https://doi.org/10.1016/j.comnet.2012.10.022) | HTTP 200 |
| [Shinn (2023)](https://doi.org/10.52202/075280-0377) | HTTP 200 |
| [Shneiderman (2020)](https://doi.org/10.1080/10447318.2020.1741118) | HTTP unavailable |
| [Venable (2016)](https://doi.org/10.1057/ejis.2014.36) | HTTP unavailable |
| [Xu (2025)](https://proceedings.iclr.cc/paper_files/paper/2025/hash/d29b8d53678015079e1d245c023e49d2-Abstract-Conference.html) | HTTP 200 |
| [Yao (2023)](https://openreview.net/forum?id=WE_vluYUL-X) | HTTP 200 |
| [Yuan (2025)](https://doi.org/10.1609/aaai.v39i28.35379) | HTTP 200 |

Of 24 HTTP 200 responses, two OpenReview pages were verification screens and one Elsevier response was a redirect shell. No blanket all-links-valid or all-full-text-checked claim is made.

</details>

## 13. VIVA ATTACK TEST

| Likely examiner question | Why it matters | Does the current thesis answer it? Minimum correction if needed |
|---|---|---|
| 1. What is new if RAG and acknowledgement already exist? | Tests contribution beyond integration rhetoric. | Yes: §§1.2.2/2.2.4/6.3 bound the contribution to a governance-oriented integration, inspectable construct and empirical identity finding. |
| 2. Why is this research rather than only an application build? | Tests DSR contribution/evaluation chain. | Yes: Tables3.1/3.2/6.1 link problem, design principles, artefact and bounded evaluation. |
| 3. What does 40.3% measure, and who decided the labels? | Tests construct validity. | Mostly: §5.4.2.2/§E.1 disclose researcher policy and missing adjudication. B1 must add C23's exception. |
| 4. Why does an acknowledged warning become ok in C23? | Exposes history/current-rule conflict. | Not adequately: B1 supplies the historical explanation without changing frozen results. |
| 5. Can acknowledgement hide a serious incident mislabelled warning? | Tests the actual safety boundary. | Yes: §5.4.2.2 and §6.3 state that the predicted-severity safeguard cannot independently recognise actual seriousness. |
| 6. Does 41.7% stability defeat the entire contribution? | Tests interpretation of a negative result. | Yes: §§4.4/5.6/6.3 make unstable identity a principal finding and identify a future deterministic design. |
| 7. Are 72 responses 72 independent incidents? | Tests pseudoreplication. | Yes: §§5.4.2/5.6.2 say 24 purposive cases × 3 nested runs; no population inference. |
| 8. Which evidence applies to v2? | Tests transfer of old results to changed implementation. | Yes: §5.4.2/Table 5.13/§E.7 distinguish v1 model evidence from current software tests. B1 adds the case-specific policy exception. |
| 9. Does 100% retrieval mean the advice was correct and safe? | Tests metric substitution. | Yes: Tables 5.7/5.9 and §6.2.1 explicitly deny that inference; C6 fixes the literature attribution. |
| 10. Does SUS 79.25 show reduced workload or better incident resolution? | Tests human-evidence scope. | Yes: §5.4.3/Appendix D give descriptive perception only, a small sample and wide variation. |
| 11. What consent, approval and data-handling arrangements applied? | Tests ethical provenance of the human study. | Partly: §3.1.4 supplies custody, retention and consented counts but leaves procedures/disposition unresolved. Complete B2 factually and privately where appropriate. |
| 12. Can I reproduce the frozen experiment rather than today's code? | Tests the reproducibility claim. | Partly: Table E.5 identifies relative paths/hashes but no access locator or specific frozen-source recovery record. C5 completes or qualifies these details. |
| 13. Do 180 tests/89% coverage make the deployed system secure? | Tests software versus operational proof. | Yes: §§5.1/5.2/4.3 disclose the limits of software claims, mocks, working-tree evidence and missing independent assessment. |
| 14. Does local hosting keep all incident data local? | Tests the governance boundary. | Yes: §§4.3.3/4.3.4/Figure 4.5 identify cloud-prompt and ntfy egress; the local Ollama option is distinct. |
| 15. Does acknowledgement save 27 model calls or prove less alert fatigue? | Tests combined/causal attribution. | Yes: §5.3 says 27 later calls and records continue; only default presentation changes. Workload/fatigue remain unmeasured. |

## FINAL DONE TEST

Checked means acceptable for the study's stated scope, not independently established production effectiveness. Pending items refer only to findings already identified above.

- [x] Research problem aligned.
- [x] Aim/objectives aligned.
- [x] Research questions aligned.
- [x] Hypotheses aligned — formal hypotheses not applicable; future hypotheses untested.
- [ ] Experimental design accurately described — B1 historical C23 policy exception needs explicit treatment.
- [x] C1–C4 definitions consistent — not applicable; actual C01–C24 are scenarios.
- [x] Causal claims defensible within stated descriptive boundaries.
- [x] Statistical analysis defensible as descriptive analysis.
- [ ] Metrics appropriately interpreted — B1 healthy-case classification and C5 timing qualification pending.
- [x] Numbers consistent where derivable; raw-record verification limits disclosed.
- [ ] Implementation claims accurate — C1/C2 documentation harmonisation pending.
- [x] Reference architecture separated from implemented system.
- [x] Literature gap defensible as scoped, non-exhaustive distinction.
- [ ] Citations/reference list consistent — pairs reconcile; C6/C9 source-characterisation wording pending.
- [x] Abstract aligned with final reported findings.
- [x] Results aligned with conclusion.
- [ ] Limitations adequate — B1 historical exception and C5 reproduction limits need consolidation.
- [x] Requirements defensible within stated evidence classes.
- [ ] Figures/tables/captions consistent — navigation/layout pass; C7 diagram order and identified table wording need correction.
- [ ] Editorial quality acceptable — final minor correction group pending.
- [x] No inappropriate reviewer-response material.
- [ ] No unresolved examiner-level issue — B1 and B2 remain open.

**FINAL STATUS: REQUIRES SIGNIFICANT REVISION**
