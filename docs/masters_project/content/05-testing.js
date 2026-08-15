const {
  p, chapterLabel, h2, h3, blank, buildTable, image,
  figureCaption, tableCaption,
} = require('../helpers');

function chapter5() {
  const b = [];

  b.push(chapterLabel('CHAPTER FIVE: TESTING, RESULTS AND EVALUATION'));
  b.push(blank());

  b.push(p('The reported results come from the current repository. The automated suite and line coverage were measured on 13 August 2026. The acknowledgement comparison uses a deterministic scenario derived from the implemented suppression rule. Live-model diagnostic quality and practitioner usability were not measured.'));

  b.push(h2('5.1  Testing Strategy'));
  b.push(p('The implemented behaviour is tested at three levels: unit tests for individual functions, API integration tests through the FastAPI application, and focused tests for acknowledgement invariants. External HTTP services and provider clients are mocked so that the suite is repeatable and does not require credentials.'));

  b.push(h3('5.1.1  Unit Tests'));
  b.push(p('Unit tests cover telemetry parsing, structured error returns, provider dispatch, verdict parsing, fingerprint generation, fallback-signature normalisation, deterministic threat detection, and selected runbook helpers. Mock responses represent Loki, Prometheus, HTTP endpoints, Docker, and provider clients.'));

  b.push(h3('5.1.2  API and Persistence Tests'));
  b.push(p('FastAPI tests exercise login, authenticated routes, rate limiting, security headers, configuration output, threat routes, verdict history, acknowledgements, and staleness reporting. Persistence tests use temporary SQLite databases to verify inserts, retention pruning, acknowledgement expiry, suppression, and removal.'));

  b.push(h3('5.1.3  Acknowledgement Invariants'));
  b.push(p('The memory tests verify that identical signature, prompt-version, and model inputs produce the same fingerprint; changing any of those inputs produces a different fingerprint; fallback signatures remove volatile tokens; an active acknowledgement can suppress only ok or warning verdicts; expired acknowledgements are inactive; and high or critical verdicts remain visible.'));

  b.push(h2('5.2  Automated Test Results'));
  b.push(p('The verification command ran pytest with coverage enabled for the agent and API packages. All 80 tests passed. Pytest reported 18 dependency deprecation warnings and no failures. Overall line coverage was 66 percent across 1,470 statements. Because coverage varies by module, Table 5.1 reports the module figures with the overall result.'));

  b.push(h3('5.2.1  Coverage by Module'));
  const covColWidths = [4200, 2200, 2626];
  const covRows = [
    ['Module', 'Line Coverage', 'Interpretation'],
    ['agent/memory.py', '100%', 'Acknowledgement fingerprint and fallback signature'],
    ['agent/orchestrator.py', '94%', 'LangGraph workflow and routing'],
    ['api/store.py', '94%', 'Verdict and acknowledgement persistence'],
    ['agent/llm/schema.py', '95%', 'Verdict parsing and severity validation'],
    ['agent/llm/providers.py', '93%', 'Provider selection and dispatch'],
    ['api/middleware/security.py', '100%', 'Response-header middleware'],
    ['api/middleware/rate_limit.py', '100%', 'Rate-limit configuration'],
    ['api/middleware/audit.py', '97%', 'Request audit middleware'],
    ['api/main.py', '79%', 'API routes and middleware integration'],
    ['api/auth.py', '82%', 'Session creation and validation'],
    ['agent/tools/loki.py', '85%', 'Loki adapter'],
    ['agent/tools/prometheus.py', '80%', 'Prometheus adapter'],
    ['agent/tools/docker_logs.py', '81%', 'Container log filtering'],
    ['agent/tools/http_probe.py', '70%', 'Endpoint probes'],
    ['agent/tools/threat_response.py', '67%', 'Threat detection and CrowdSec adapter'],
    ['agent/llm/langchain_agent.py', '15%', 'Multi-tool provider path'],
    ['agent/rag/vector_store.py', '31%', 'ChromaDB integration'],
    ['agent/rag/local_runbooks_loader.py', '89%', 'Local Markdown runbook loading'],
    ['agent/llm/gemini_client.py', '88%', 'Direct Gemini API integration'],
    ['agent/main.py', '0%', 'Long-running heartbeat entry point'],
    ['OVERALL', '66%', '80 passing tests; 1,470 statements'],
  ];
  b.push(buildTable(covColWidths, covRows));
  b.push(tableCaption('Table 5.1: Test Coverage Summary by Module, measured on 13 August 2026.'));
  b.push(image('figures/fig_5_1_acceptance.png', { w: 6.1, h: 3.90 }));
  b.push(figureCaption('Figure 5.1: Selected Module Coverage from the Verification Run.'));

  b.push(h3('5.2.2  Representative Test Cases'));
  const tcColWidths = [900, 3200, 3400, 1526];
  const tcRows = [
    ['ID', 'Scenario', 'Expected Outcome', 'Result'],
    ['TC-01', 'Loki range query returns multiple streams', 'Recent lines are parsed in newest-first order', 'Pass'],
    ['TC-02', 'Prometheus collection', 'Configured metric keys are returned', 'Pass'],
    ['TC-03', 'HTTP probe', 'Status and latency are recorded for each URL', 'Pass'],
    ['TC-04', 'Critical verdict routing', 'Notification path is selected', 'Pass'],
    ['TC-05', 'OK verdict routing', 'Notification path is skipped', 'Pass'],
    ['TC-06', 'Fingerprint stability', 'Identical inputs yield the same fingerprint', 'Pass'],
    ['TC-07', 'Fingerprint mismatch', 'Signature, prompt, or model change yields a different fingerprint', 'Pass'],
    ['TC-08', 'Severity safeguard', 'High and critical verdicts are not suppressed', 'Pass'],
    ['TC-09', 'Warning acknowledgement', 'Matching warning is marked acknowledged and suppressed', 'Pass'],
    ['TC-10', 'Expired acknowledgement', 'Expired row is not active', 'Pass'],
    ['TC-11', 'Critical acknowledgement request', 'API returns HTTP 409', 'Pass'],
    ['TC-12', 'Retention pruning', 'Rows outside the window are removed on insert', 'Pass'],
    ['TC-13', 'HTTP brute-force fixture', 'Threshold crossing produces a threat record', 'Pass'],
    ['TC-14', 'Login rate limit', 'Sixth rapid failed attempt returns HTTP 429', 'Pass'],
    ['TC-15', 'Stale verdict', 'Old verdict is reported as stale', 'Pass'],
    ['TC-16', 'Configuration response', 'Only integration booleans are returned', 'Pass'],
  ];
  b.push(buildTable(tcColWidths, tcRows));
  b.push(tableCaption('Table 5.2: Representative Automated Test Cases and Results.'));

  b.push(h2('5.3  Acknowledgement-Memory Evaluation'));
  b.push(p('The acknowledgement feature changes the display of repeated low-risk verdicts. In the 30-cycle scenario, the same warning fingerprint is stored once per cycle. Without an acknowledgement, 30 rows remain visible. When the operator acknowledges the condition after cycle 3, the remaining 27 cycles still call the model and store a verdict, but the matching warnings are hidden in the default view. The visible cumulative count stays at 3. Figure 5.2 plots the comparison, while TC-08 and TC-09 test the rules used by the scenario.'));
  b.push(image('figures/fig_5_2_mttr.png', { w: 6.1, h: 3.58 }));
  b.push(figureCaption('Figure 5.2: Visible Duplicate Warnings with and without an Acknowledgement.'));
  b.push(p('This result supports a narrow conclusion: the feature reduces repeated operator-facing warnings in the default dashboard view. It does not reduce the number of model calls, the number of stored heartbeat results, or inference cost.'));

  b.push(h2('5.4  Evaluation Work Not Completed'));
  b.push(h3('5.4.1  Live-Model Diagnostic Quality'));
  b.push(p('The present suite does not measure whether live model verdicts identify the correct root cause, assign the correct severity, or remain faithful to the supplied evidence. A later study should use labelled telemetry scenarios and report schema-valid response rate, severity accuracy, supported-claim rate, false positives, false negatives, latency, and provider cost. Results should be reported separately for each provider and model version.'));
  b.push(h3('5.4.2  Practitioner Usability'));
  b.push(p('The task script and System Usability Scale questionnaire in Appendix D were prepared but were not administered as part of the evidence available for this report. No participant count, completion time, SUS score, interview finding, or interface improvement is claimed.'));

  b.push(h2('5.5  Evaluation Against the Objectives'));
  const evColWidths = [700, 3000, 3600, 1726];
  const evRows = [
    ['Obj.', 'Objective', 'Evidence and Qualification', 'Status'],
    ['O-1', 'Multi-source telemetry collection.', 'Loki, Prometheus, HTTP, and optional Docker adapters are implemented and tested with mocked upstreams.', 'Achieved'],
    ['O-2', 'Structured LLM reasoning workflow.', 'The graph, provider dispatch, parser, and routing are implemented and tested. Live diagnostic accuracy was not evaluated.', 'Partly achieved'],
    ['O-3', 'Runbook retrieval and operator-approved threat response.', 'Local runbook loading and threat logic are tested; ChromaDB and live CrowdSec paths still have limited coverage.', 'Partly achieved'],
    ['O-4', 'Fingerprint-based acknowledgement memory.', 'Fingerprint, expiry, API suppression, removal, and severity safeguards are covered by tests and the deterministic comparison.', 'Achieved'],
    ['O-5', 'Single-host packaging and evaluation.', 'Docker Compose and CI files are present; 80 tests pass. Usability and production-security validation remain outstanding.', 'Partly achieved'],
  ];
  b.push(buildTable(evColWidths, evRows));
  b.push(tableCaption('Table 5.3: Objective and Evidence Matrix.'));

  b.push(h2('5.6  Discussion and Threats to Validity'));
  b.push(h3('5.6.1  Supported Findings'));
  b.push(p('The evidence covers the implemented control flow, provider dispatch, response parsing, persistence, acknowledgement rules, selected API protections, and deterministic threat thresholds. The acknowledgement tests also confirm that repeated low-risk verdicts can be hidden from the default view while high and critical verdicts remain visible.'));
  b.push(h3('5.6.2  Limitations'));
  b.push(p('Several operational paths still have limited automated coverage, including the heartbeat entry point, live provider API calls, ChromaDB integration, and much of the LangChain multi-tool path. Tests use mocks for external services. The evaluation does not establish model accuracy, cost, latency, operator trust, or usability. The fallback condition signature is heuristic and may merge distinct conditions or split equivalent ones. The supplied deployment also requires network and TLS hardening before production use.'));
  b.push(h3('5.6.3  Validity'));
  b.push(p('Construct validity is limited because passing software tests are not a measure of diagnostic correctness. Internal validity is strengthened by repeatable fixtures but weakened by extensive mocking. External validity is limited to the tested single-host design; no multi-host or practitioner field study was conducted. The repository, command, date, test count, warning count, and coverage values are stated so the measured results can be reproduced.'));

  return b;
}

module.exports = { chapter5 };
