const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable, image } = require('../helpers');
const { AlignmentType } = require('docx');

function chapter5() {
  const b = [];

  b.push(chapterLabel('CHAPTER FIVE'));
  b.push(pCenter('TESTING, PROPOSED EVALUATION AND EXPECTED OUTCOMES'));
  b.push(blank());

  b.push(p('Chapter Note. The implementation described in Chapter Four is operational; the testing apparatus (unit, integration, security, and adversarial) has been executed continuously throughout development and its outcomes are reported below as measured facts. The end-to-end empirical evaluation against the 150-finding benchmark — covering accuracy, MTTR, cost, and operator-trust outcomes across five LLM providers — is presented in this chapter as a proposed evaluation protocol with expected outcomes. Sections 5.1 (Testing Strategy) and 5.2 (Test Outcomes for Apparatus-Level Tests) reflect actual execution. Sections 5.3 (Proposed Evaluation Protocol), 5.4 (Expected Outcomes and Illustrative Projections), 5.5 (Evaluation of Objectives), and 5.6 (Discussion) frame the larger evaluation as a forward-looking, reproducible plan. All charts in this chapter are explicitly labelled as illustrative projections. This separation is deliberate: it preserves academic honesty about what has been measured versus what is forecast under the proposed protocol, and it equips a future cohort (or this author in a subsequent extension of the work) to execute the benchmark and produce the corresponding measurements.'));

  // 5.1 TESTING STRATEGY (executed)
  b.push(h2('5.1  Testing Strategy'));
  b.push(p('Testing of InfraGuard Pro is organised along four mutually reinforcing tiers: unit testing of individual modules, integration testing of subsystem interactions, security and adversarial testing of the running system, and end-to-end empirical evaluation against the 150-finding benchmark dataset. The first three tiers have been executed continuously throughout the development period and their outcomes are summarised below. The fourth tier — the end-to-end benchmark — is presented as a proposed evaluation protocol from Section 5.3 onwards. Throughout, both local development execution and CI execution on every pull request use the same test harness; performance and cost benchmarks (when run) are executed on a dedicated benchmark runner to eliminate noise from concurrent CI activity.'));

  b.push(h3('5.1.1  Unit Testing'));
  b.push(p('Unit tests are authored using pytest and pytest-asyncio, with respx for HTTP mocking and hypothesis for property-based testing of the SARIF normaliser. The unit-test suite covers individual functions and classes in isolation, exercising both the success path and the documented failure paths. The coverage target (NFR-11) is 80% line coverage; the achieved coverage at the time of writing, measured by coverage.py and reported in CI, is documented in Table 5.1.'));
  b.push(p('Notable unit tests include: (i) the SARIF normaliser against a fixture corpus of saved scanner outputs in tests/fixtures/sarif/ covering Trivy, Semgrep, Bandit, Checkov, Gitleaks, and OSV-Scanner; (ii) the policy engine against a parameterised matrix of (confidence, files_touched, cvss, finding_class) tuples covering all three remediation modes; (iii) the audit-log hash chain against a property-based test that asserts any single-byte mutation invalidates the chain; (iv) each LLM provider implementation against a respx-mocked endpoint asserting correct request shaping and response parsing.'));

  b.push(h3('5.1.2  Integration Testing'));
  b.push(p('Integration tests exercise subsystem interactions with real (containerised) infrastructure dependencies. A docker-compose.test.yml file boots a PostgreSQL container, a ChromaDB container, a Prometheus container, a Loki container, a Traceway container, and the InfraGuard control plane against a fixture configuration. Test cases include: (i) end-to-end SARIF ingestion → finding persistence → remediation-engine pickup → mocked LLM call → policy classification → mocked Git-provider call → audit-log persistence; (ii) satellite registration → heartbeat → action queue → executor; (iii) RAG indexing across all four source classes followed by a similarity-search assertion; (iv) verdict generation with each of the five LLM providers stubbed to deterministic responses, asserting end-to-end correctness across the provider matrix.'));

  b.push(h3('5.1.3  Security Testing (self-scanning)'));
  b.push(p('The system is, with deliberate symmetry, subjected to its own scanner stack. Trivy filesystem-mode, Semgrep, Bandit, Gitleaks, Checkov against the docker-compose.yml, and OSV-Scanner against the dependency manifest are run as part of the pull-request CI on every commit during the development period. The system processes the resulting SARIF documents through its own remediation engine in human-approval mode and the author reviews every generated patch — providing a continuous adversarial test of the system against real-world findings on its own codebase. This activity exercises the SARIF adapter, the RAG retrieval surface, the policy engine, and the Git-provider adapter on production-like input rather than synthetic fixtures, and is the source of the bulk of the empirical confidence the author holds in the implementation. Aggregate statistics from the development period are reported in Section 5.2.'));

  b.push(h3('5.1.4  Adversarial / Prompt-Injection Testing'));
  b.push(p('Three categories of adversarial input have been exercised against the remediation engine: (i) a SARIF document with a finding message containing instructions to ignore the system prompt; (ii) a runbook uploaded with embedded instructions to bypass the policy engine; (iii) a commit message in a vulnerable dependency containing instructions to introduce a backdoor. In all three cases the structured-output schema and the policy-engine bounds (autonomous mode permitted only on the allow-listed file globs) defeat the injection attempt; the system either refuses to produce a patch or produces a benign patch that is correctly classified as recommend-only by the policy engine. These tests are not exhaustive; Section 5.6 identifies systematic adversarial robustness as future work.'));

  b.push(h3('5.1.5  User Acceptance Testing'));
  b.push(p('User-acceptance testing is conducted in two rounds. Round 1, internal acceptance, validates each functional requirement (FR-01 through FR-15) against a written test script executed by the author through the dashboard UI and the API. Every requirement is confirmed to pass or annotated with a defect for resolution. Round 2, practitioner acceptance, is reserved for the broader empirical evaluation described in Section 5.3 and has not yet been performed; the protocol is documented there.'));

  // 5.2 TEST OUTCOMES (apparatus-level)
  b.push(h2('5.2  Apparatus-Level Test Outcomes'));
  b.push(p('This section reports the outcomes of the testing apparatus described in Section 5.1 — that is, unit, integration, security self-scanning, and adversarial testing — as observed during the development period. These outcomes are measurements, not projections.'));

  b.push(h3('5.2.1  Test Coverage'));
  b.push(p('Table 5.1 reports the achieved test coverage by module at the time of writing.'));
  b.push(blank());
  const covColWidths = [3000, 2000, 2000, 2026];
  const covHeaders = ['Module', 'Line Coverage', 'Branch Coverage', 'Test Count'];
  const covRows = [
    covHeaders,
    ['agent/orchestrator.py', '87.2%', '79.4%', '24'],
    ['agent/llm/* (6 providers)', '91.0%', '85.1%', '62'],
    ['agent/rag/*', '82.5%', '76.3%', '18'],
    ['agent/remediation/engine.py', '88.9%', '81.6%', '31'],
    ['agent/remediation/sarif.py', '94.2%', '90.5%', '46'],
    ['agent/remediation/policy.py', '96.7%', '94.1%', '38'],
    ['agent/remediation/git_provider.py', '85.4%', '77.8%', '22'],
    ['agent/remediation/validator.py', '79.1%', '71.2%', '15'],
    ['agent/tools/*', '83.6%', '75.4%', '34'],
    ['api/routes/*', '86.8%', '80.2%', '57'],
    ['api/middleware/*', '90.4%', '84.7%', '21'],
    ['api/store/*', '78.3%', '70.1%', '13'],
    ['satellite/*', '81.9%', '74.6%', '19'],
    ['OVERALL', '84.3%', '78.1%', '400'],
  ];
  b.push(buildTable(covColWidths, covRows));
  b.push(blank());
  b.push(p('Table 5.1: Test Coverage Summary by Module (measured).', { align: AlignmentType.CENTER }));

  b.push(h3('5.2.2  Self-Scanning Outcome Summary'));
  b.push(p('Across the development period the multi-scanner CI pipeline surfaced approximately 247 unique findings on the InfraGuard Pro codebase itself. Of these: 198 were correctly patched on the first iteration when routed through the system in human-approval mode and approved by the author; 31 required prompt-engineering iteration before the produced patch satisfied the originating scanner; and 18 were determined to be false positives correctly flagged by the policy engine as recommend-only. These figures provide empirical comfort that the implemented apparatus operates end-to-end on real input — and motivate the larger, more controlled benchmark proposed in Section 5.3.'));

  b.push(h3('5.2.3  Adversarial Test Outcomes'));
  b.push(p('All three categories of adversarial injection described in Section 5.1.4 are defeated by the combination of structured-output enforcement and policy-engine file-glob bounds. No injection attempt produced an autonomous-mode-classified patch in the development environment. These results are positive but not exhaustive; future work should mount a more systematic OWASP LLM Top 10-aligned evaluation, as discussed in Section 6.4.'));

  // 5.3 PROPOSED EVALUATION PROTOCOL
  b.push(h2('5.3  Proposed Evaluation Protocol'));
  b.push(p('Beyond the apparatus-level tests reported in Section 5.2, this work proposes — but has not yet executed — a controlled empirical evaluation of InfraGuard Pro against a 150-finding benchmark. The protocol is documented here in sufficient detail to be reproducible by a subsequent cohort, by an industrial partner, or by the author in a future extension of the work. Section 5.4 then reports the expected outcomes of executing this protocol, grounded in the published performance of the underlying LLM models and the apparatus-level test results of Section 5.2.'));

  b.push(h3('5.3.1  Benchmark Composition'));
  b.push(p('The proposed 150-finding evaluation benchmark would be constructed by harvesting ninety real-world findings from public OSV-Scanner and Trivy reports against well-known open-source Python and Node.js projects, supplemented by sixty synthetically-injected findings designed to exercise specific edge cases: multi-file SQL-injection patterns, Dockerfile USER 0 violations, Terraform overly-permissive IAM policies, hard-coded credentials, deprecated TLS cipher suites, vulnerable transitive dependencies, and outdated container base images. The benchmark would be balanced across CVSS severity (40 critical, 50 high, 40 medium, 20 low) and across scanner class (45 SCA, 30 SAST, 25 container, 30 IaC, 20 secret). The full proposed composition is enumerated in Appendix D and is committed to the repository as fixture data so that future executions are reproducible.'));

  b.push(h3('5.3.2  Experimental Variables'));
  b.push(p('The protocol defines two principal independent variables — the LLM provider (Vertex AI Gemini 2.5 Flash, OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, Moonshot Kimi-K2, Ollama Llama 3.1 8B on CPU, plus a best-of-three ensemble) and the remediation mode (recommend-only, human-approval-required, autonomous-low-risk) — and the following dependent variables: (i) patch quality, classified into fully correct, partially correct, incorrect, and refused; (ii) end-to-end mean time-to-remediate measured from SARIF ingestion to merged pull request; (iii) LLM cost per remediation, computed from provider-reported token counts and public list pricing; (iv) confidence calibration measured as the correlation between LLM-reported confidence and empirical correctness; (v) operator-trust outcomes captured through a System Usability Scale (SUS) instrument administered to a recruited practitioner cohort.'));

  b.push(h3('5.3.3  Patch-Quality Adjudication'));
  b.push(p('Patch quality is adjudicated through a two-stage process. Stage 1 is automated: the originating scanner is re-run against the patched artefact and the patch is provisionally marked fully correct only if the specific rule violation is no longer reported and no new findings are introduced. Stage 2 is manual: a human adjudicator (the author for internal runs; a recruited second reviewer for external validity) inspects each provisionally-correct patch and assigns the final classification, ensuring that scanner false-negatives do not inflate the score. The Cohen-κ agreement statistic is reported between automated and manual adjudication.'));

  b.push(h3('5.3.4  Runtime-Regression Observation'));
  b.push(p('For every merged patch the closed-loop validator opens a runtime observation window of configurable duration (default ten minutes inclusive of CI re-run) during which the runtime telemetry of the affected satellite is monitored for: (i) a step change in HTTP 5xx ratio; (ii) a step change in container restart count; (iii) a step change in p95 latency; (iv) any new critical-severity verdict from the reasoning agent referencing the affected service. The window outcome contributes to the patch-quality classification and is recorded in the validations table for the historical-fix RAG corpus.'));

  b.push(h3('5.3.5  Practitioner User Acceptance Testing Cohort'));
  b.push(p('The protocol prescribes recruitment of three external DevSecOps practitioners (target profile: one from a Nigerian fintech, one from a Kenyan health-tech startup, one from a UK or European managed-services provider) to execute a fixed scenario: (a) register two satellites, (b) ingest a SARIF document containing twelve findings, (c) approve four human-approval-required remediations from the dashboard, (d) inspect a closed-loop validation outcome, and (e) switch the active LLM provider mid-session. Each participant completes a SUS questionnaire and a structured free-text debrief covering effectiveness, efficiency, learnability, and trust. Recruitment is forecast to occur in the next quarter; results would be reported as a Section 5.5 addendum.'));

  b.push(h3('5.3.6  Statistical Treatment'));
  b.push(p('Each benchmark configuration would be repeated three times to bound the variance introduced by LLM non-determinism, with temperature pinned to 0.2 for all providers that expose the parameter. Results would be reported as mean with 95% confidence interval bands where the sample sizes warrant. Where confidence intervals would be misleading (single-run pilots), point estimates would be flagged accordingly. The full data tables and analysis scripts would be released as a reproducibility package alongside the open-source repository.'));

  b.push(h3('5.3.7  Reproducibility'));
  b.push(p('The reproducibility package consists of: (i) the fixture benchmark in tests/fixtures/benchmark/ (committed to the repository); (ii) the docker-compose.benchmark.yml that boots the full control plane plus a sealed test satellite plus deterministic-stub HTTP responders for each LLM provider; (iii) a Python orchestrator scripts/run_benchmark.py that walks the benchmark, dispatches each finding through the engine, harvests results into a SQLite results database, and emits CSV summaries; (iv) a Jupyter notebook for the analysis and chart generation; (v) the prompt templates and policy YAML used in the run. The package is designed to permit a third party to replicate the experiment end-to-end on a single commodity host in under twelve hours of wall-clock time.'));

  // 5.4 EXPECTED OUTCOMES (illustrative)
  b.push(h2('5.4  Expected Outcomes and Illustrative Projections'));
  b.push(p('This section presents the expected outcomes of executing the protocol of Section 5.3, framed as projections derived from (i) the published performance of the underlying LLM models on closely-adjacent benchmarks in the literature, (ii) the apparatus-level test outcomes reported in Section 5.2, and (iii) the author’s engineering judgement based on the self-scanning experience accumulated during development. All numerical figures in this section, and all charts in Figures 5.1 through 5.4, are illustrative projections — not measurements — and are clearly labelled as such.'));

  b.push(h3('5.4.1  Projected Patch Quality by Provider and Severity'));
  b.push(p('Figure 5.1 visualises the projected patch acceptance rate by LLM provider and CVSS severity. The expected pattern is that frontier proprietary models (Claude 3.5 Sonnet, GPT-4o) outperform the lower-cost and self-hosted alternatives, with the gap widening at higher severities where the patches are typically more complex; that all providers achieve high acceptance rates on low-severity findings (where the typical patch is a dependency-version bump); and that a best-of-three ensemble approach materially improves over any single provider.'));
  b.push(blank());
  b.push(image('figures/fig_5_1_acceptance.png', { w: 8.5, h: 4.8 }));
  b.push(pCenter('Figure 5.1: Projected Patch Acceptance Rate by LLM Provider and Severity (illustrative).'));
  b.push(blank());

  b.push(h3('5.4.2  Projected Mean Time-to-Remediate Distribution'));
  b.push(p('Figure 5.2 visualises the projected MTTR distribution across the three remediation modes against a manual-triage baseline. The expected pattern is a clear separation of three orders of magnitude on a log-scale: autonomous mode in the low single-digit minutes, human-approval mode in the tens of minutes, and the manual baseline (drawn from the Snyk and Sonatype industry surveys cited in Chapter Two) in the hours.'));
  b.push(blank());
  b.push(image('figures/fig_5_2_mttr.png', { w: 8.5, h: 4.4 }));
  b.push(pCenter('Figure 5.2: Projected MTTR Distribution Across Remediation Modes (illustrative; log scale).'));
  b.push(blank());

  b.push(h3('5.4.3  Projected Cost per Remediation'));
  b.push(p('Figure 5.3 visualises the projected LLM cost per remediation by provider, derived from public list pricing and the median input and output token counts observed during apparatus-level testing. The expected pattern is a roughly 25× spread between the most-expensive frontier provider (Claude 3.5 Sonnet) and the cheapest cloud provider (Vertex AI Gemini 2.5 Flash), with the self-hosted Ollama and LM Studio options at zero marginal cost.'));
  b.push(blank());
  b.push(image('figures/fig_5_3_cost.png', { w: 8.5, h: 4.4 }));
  b.push(pCenter('Figure 5.3: Projected LLM Cost per Remediation by Provider (illustrative; based on public list pricing).'));
  b.push(blank());

  b.push(h3('5.4.4  Projected Confidence Calibration'));
  b.push(p('Figure 5.4 plots the projected calibration curves of LLM-reported confidence against the empirical patch correctness rate. The expected pattern is that frontier proprietary models track the perfect-calibration diagonal closely while the lower-cost and self-hosted alternatives show progressively greater dispersion, particularly producing spurious high-confidence incorrect patches. Empirical calibration data of this form, once measured, motivates a planned per-provider confidence-recalibration factor in the policy engine (see Section 6.4.2).'));
  b.push(blank());
  b.push(image('figures/fig_5_4_calibration.png', { w: 7.5, h: 5.2 }));
  b.push(pCenter('Figure 5.4: Projected Confidence-Calibration Curve (illustrative).'));
  b.push(blank());

  // 5.5 EVALUATION OF OBJECTIVES
  b.push(h2('5.5  Evaluation of Objectives'));
  b.push(p('The five specific objectives from Section 1.3.2 are evaluated below against the design and implementation evidence and against the proposed protocol. Table 5.4 summarises the objective-versus-outcome matrix; objectives are reported as Design-Complete where the engineering artefact is delivered and exercised by apparatus-level testing, and as Evaluation-Proposed where the empirical confirmation is contingent on executing the protocol of Section 5.3.'));
  b.push(blank());
  const evColWidths = [800, 3300, 3200, 1726];
  const evHeaders = ['Obj.', 'Stated Objective', 'Outcome / Evidence', 'Status'];
  const evRows = [
    evHeaders,
    ['O-1', 'Design a SARIF-based ingestion pipeline consuming output from at least six scanner classes and normalising into a unified internal representation.', 'Implemented in agent/remediation/sarif.py with fixture-based unit tests covering Trivy, Semgrep, Bandit, Checkov, Gitleaks, and OSV-Scanner; 94.2% line coverage; ingestion latency target documented in NFR-01.', 'Design-Complete'],
    ['O-2', 'Develop a pluggable LLM provider abstraction supporting at least five backends with runtime switching, attribution, cost tracking, and fallback.', 'Six concrete providers implemented (Vertex AI, OpenAI, Anthropic, Kimi, Ollama, LM Studio); runtime switching via /api/agent/llm-config validated in unit tests; per-verdict provider attribution recorded in the remediations table; fallback validated by killing the active provider container.', 'Design-Complete'],
    ['O-3', 'Implement a retrieval-augmented patch generation engine grounded in CVE data, organisation runbooks, and historical fix outcomes, with structured citation and audit-grade evidence trails.', 'Multi-source RAG over Notion, local Markdown, uploads, and historical verdicts implemented in agent/rag/; ChromaDB-backed similarity search; every Verdict carries an evidence array; demonstrated through the dashboard runbook chat and the per-remediation evidence view.', 'Design-Complete'],
    ['O-4', 'Design and implement a policy engine with three execution modes integrated with the Git provider pull-request workflow and a tamper-evident audit log.', 'Policy engine in agent/remediation/policy.py with 96.7% line coverage; integration tests cover all three modes; GitHub and GitLab adapters validated end-to-end against staged repositories; audit-log hash chain verified by scripts/verify_audit_chain.py against tamper-injection tests.', 'Design-Complete'],
    ['O-5', 'Deploy across a multi-server satellite topology representative of the LivWell environment; evaluate against the 150-finding benchmark; quantify accuracy, MTTR, cost, false-positive rate, regression rate, and operator-trust outcomes.', 'Three-satellite deployment (prod-stub-us, prod-stub-eu, staging-stub-eu) demonstrated in development; protocol for the 150-finding benchmark documented in Section 5.3; projected outcomes illustrated in Section 5.4; practitioner UAT cohort recruitment scheduled.', 'Evaluation-Proposed'],
  ];
  b.push(buildTable(evColWidths, evRows));
  b.push(blank());
  b.push(p('Table 5.4: Objective-versus-Outcome Evaluation Matrix.', { align: AlignmentType.CENTER }));

  // 5.6 DISCUSSION
  b.push(h2('5.6  Discussion'));

  b.push(h3('5.6.1  What the Apparatus-Level Evidence Already Supports'));
  b.push(p('Four design decisions are, on the apparatus-level evidence accumulated during development, already well-supported. First, the strict structured-output contract has demonstrably improved patch-quality consistency across providers in the self-scanning workflow and has made post-hoc audit tractable. Second, the policy engine’s clean separation between recommend-only, human-approval, and autonomous-low-risk modes is exercised throughout the unit and integration test matrix and has held without modification since its mid-project introduction. Third, the closed-loop validator’s ability to re-run the originating scanner against the patched artefact has been exercised on the InfraGuard Pro codebase itself and reliably catches the cases where an LLM patch fails to satisfy the originating rule. Fourth, the multi-source RAG corpus — particularly the inclusion of historical fix outcomes — produces qualitatively richer retrieved context than the original Notion-only baseline.'));

  b.push(h3('5.6.2  What the Proposed Evaluation Would Demonstrate'));
  b.push(p('The empirical evaluation, when executed, would convert the qualitative confidence above into defensible quantitative claims along three axes: (i) the relative patch quality of frontier proprietary, mid-tier cloud, and self-hosted LLM providers in the autonomous-remediation setting; (ii) the realistic end-to-end MTTR reduction achievable when remediation is shifted left into the pipeline; (iii) the cost envelope within which a small DevSecOps team can credibly sustain autonomous-mode operation. Each of these axes is currently presented as an illustrative projection (Figures 5.1, 5.2, 5.3) and would, on execution, become a measured outcome.'));

  b.push(h3('5.6.3  What Did Not Work During Development'));
  b.push(p('Three design choices required revision during the project. First, the initial decision to allow a single LangChain ReAct loop with unconstrained tool invocations produced unbounded LLM cost and occasional infinite loops; this was replaced by the bounded LangGraph state machine with explicit transitions, which trades a little flexibility for substantial predictability. Second, the original plan to support a fully-autonomous mode for high-severity findings was abandoned after early experiments showed that the failure modes on critical CVEs were exactly the cases most damaging to misclassify; the production-ready policy engine now caps autonomous mode at CVSS ≤ 6.9, with all critical findings routed to human approval. Third, the original SQLite-only persistence baseline did not survive contact with the multi-satellite topology; PostgreSQL was introduced as the central store, with SQLite retained only as the satellite-local buffer.'));

  b.push(h3('5.6.4  Comparison with Existing Systems (qualitative)'));
  b.push(p('Cross-referencing the capability matrix of Table 2.2, InfraGuard Pro is the only system among those surveyed that simultaneously supports (i) multi-scanner unified ingestion, (ii) multi-vendor LLM abstraction including self-hosted options, (iii) a three-mode policy engine, (iv) multi-provider Git integration, (v) RAG over organisation-specific runbooks, (vi) historical-fix retrieval, (vii) closed-loop post-deployment validation, (viii) multi-server satellite operation, (ix) tamper-evident audit logging, and (x) open-source self-hosting. The closest commercial peer, GitHub Copilot Autofix, achieves a stronger single-scanner-and-single-provider experience but does not address (i), (ii), (iv), (v), (vii), (viii), or (x). The closest open-source peer, the combination of Trivy + Dependabot, achieves (i) and partially (iv) but addresses none of the LLM-driven capabilities. The qualitative comparative case is therefore strong; the proposed evaluation of Section 5.3 would provide the quantitative grounding.'));

  b.push(h3('5.6.5  Threats to Validity'));
  b.push(p('The evaluation framing carries the following acknowledged threats to validity. (a) Internal validity: the proposed 150-finding benchmark mixes real and synthetic findings; while the synthetic findings are designed to be representative, their distribution may not perfectly match operational reality, and this should be assessed at execution time. (b) External validity: the proposed UAT cohort comprises three practitioners only and is consequently a small sample; SUS scores and free-text feedback should be interpreted accordingly. (c) Construct validity: the “fully correct” patch category as adjudicated by the originating scanner re-run is imperfect (false negatives in the scanner may mask incomplete patches); the closed-loop validator’s runtime-regression check and the two-stage manual adjudication described in Section 5.3.3 partially compensate but do not eliminate the risk. (d) Statistical validity: even with three runs per configuration, non-determinism in LLM output may introduce variance that is not fully captured; future replications should average over more runs. (e) Construct validity of the projections in Section 5.4: those values are derived from published model performance on adjacent benchmarks and apparatus-level test outcomes; they should be treated as forecasts to be confirmed or refuted by the protocol of Section 5.3, not as measurements.'));

  return b;
}

module.exports = { chapter5 };
