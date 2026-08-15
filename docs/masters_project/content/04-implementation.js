const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable, image, figureCaption, tableCaption } = require('../helpers');

function chapter4() {
  const b = [];

  b.push(chapterLabel('CHAPTER FOUR: SYSTEM IMPLEMENTATION'));
  b.push(blank());

  // 4.1 DEVELOPMENT ENVIRONMENT
  b.push(h2('4.1  Development Environment'));
  b.push(p('Development and validation were carried out on a workstation configured to approximate the target single-host deployment.'));

  b.push(h3('4.1.1  Hardware and Operating System'));
  b.push(p('Primary development was conducted on a Windows 11 workstation running Docker Desktop. All services run in Linux containers based on the python:3.11-slim image. The target production environment is a single Google Compute Engine virtual machine running native Docker, provisioned through Terraform.'));

  b.push(h3('4.1.2  Source Control and Continuous Integration'));
  b.push(p('Two GitHub Actions workflows are defined. test.yml runs the pytest suite for pull requests to the main branch. deploy.yml runs its own test step on a push to main before building the agent and API images, publishing them to Google Artifact Registry, and updating the target virtual machine. The deployment is therefore conditional on the test step within the same job.'));

  b.push(h3('4.1.3  Editor and Tooling'));
  b.push(p('Development was performed in Visual Studio Code with Python and Docker tooling. Application dependencies are listed in requirements.txt and installed into each container at build time.'));

  // 4.2 IMPLEMENTATION DETAILS
  b.push(h2('4.2  Implementation Details'));
  b.push(p('The module descriptions follow the repository layout. All file paths are relative to the repository root.'));

  b.push(h3('4.2.1  Repository Layout'));
  b.push(p('Figure 4.1 visualises the folder structure of the reference implementation; the path-by-path responsibility map follows in Table 4.1.'));
  b.push(blank());
  b.push(image('figures/fig_4_1_folder.png', { w: 6.0, h: 6.5 }));
  b.push(figureCaption('Figure 4.1: Folder Structure of the InfraGuard AI Reference Implementation.'));
  b.push(blank());

  const layoutColWidths = [2600, 6426];
  const layoutRows = [
    ['Path', 'Responsibility'],
    ['agent/main.py', 'Heartbeat entry point; fetches acknowledgements, runs the cycle, persists verdicts, dispatches notifications.'],
    ['agent/orchestrator.py', 'The LangGraph state machine wiring collect_data, analyze, decide_action, and notify.'],
    ['agent/memory.py', 'Verdict fingerprinting (signature + ruleset version) and deterministic signature fallback.'],
      ['agent/llm/providers.py', 'LLM dispatch: direct Gemini (default), Anthropic Claude, OpenAI, or local Ollama via LLM_PROVIDER.'],
    ['agent/llm/schema.py', 'Shared verdict contract: system instruction, JSON extraction, and severity validation for every provider.'],
    ['agent/llm/gemini_client.py', 'Single-call Gemini Developer API client.'],
    ['agent/llm/anthropic_client.py', 'Single-call Anthropic Claude client.'],
    ['agent/llm/openai_client.py', 'Single-call OpenAI client.'],
    ['agent/llm/langchain_agent.py', 'LangChain multi-tool agent (ReAct-style) over the telemetry tools.'],
    ['agent/llm/prompts.py', 'Prompt assembly, evidence constraints, and the known-conditions memory block.'],
    ['agent/rag/local_runbooks_loader.py', 'Local Markdown discovery, metadata extraction, and document loading.'],
    ['agent/rag/vector_store.py', 'ChromaDB binding with local ONNX embeddings: index, load, and similarity search.'],
    ['agent/rag/runbook_agent.py', 'Retrieval-augmented runbook question answering.'],
    ['agent/tools/loki.py, prometheus.py, http_probe.py', 'Telemetry collection tools (logs, metrics, endpoint health).'],
    ['agent/tools/docker_api.py, docker_events.py, docker_logs.py', 'Optional Docker Engine telemetry (events, diagnostics, log tail).'],
    ['agent/tools/threat_response.py', 'Deterministic threat detection and the CrowdSec adapter.'],
    ['agent/tools/notify.py, langchain_tools.py', 'ntfy.sh notifications; @tool wrappers for the multi-tool agent.'],
    ['api/main.py', 'FastAPI application: routes, middleware registration, auth, and the acknowledgement and threat endpoints.'],
    ['api/auth.py', 'Signed session-token creation and validation.'],
    ['api/store.py', 'SQLite persistence for verdicts and acknowledgements, with retention pruning.'],
    ['api/middleware/audit.py, security.py, rate_limit.py', 'Request auditing, security headers/CSP, and rate limiting.'],
    ['dashboard/index.html, login.html', 'The single-page operations dashboard and the login page.'],
    ['tests/', 'pytest suite: test_tools, test_agent, test_api, test_store, test_memory, test_rag, test_threat_response.'],
    ['terraform/', 'Google Compute Engine infrastructure-as-code.'],
    ['docker-compose.yml, agent/Dockerfile, api/Dockerfile', 'Container composition and image definitions.'],
    ['.github/workflows/test.yml, deploy.yml', 'CI test workflow and CD deployment workflow.'],
  ];
  b.push(buildTable(layoutColWidths, layoutRows));
  b.push(blank());
  b.push(tableCaption('Table 4.1: Repository Module Map and Responsibilities.'));

  b.push(h3('4.2.2  The Reasoning Agent and LangGraph Loop'));
  b.push(p('The reasoning workflow is defined in agent/orchestrator.py and scheduled by the asyncio heartbeat in agent/main.py. At each interval, the heartbeat loads active acknowledgements and may tail a monitored container\'s error logs when Docker monitoring is enabled. It invokes the compiled LangGraph workflow on a worker thread so the blocking model call does not stop the event loop. The collect_data node gathers telemetry, analyze requests the verdict, and decide_action may add container diagnostics for a high or critical result. A conditional edge sends high and critical verdicts to notify; other verdicts end the cycle.'));

  b.push(h3('4.2.3  The Two LLM Reasoning Modes'));
  b.push(p('The agent supports two analysis modes selected by USE_LANGCHAIN_AGENT and four providers selected by LLM_PROVIDER: direct Gemini, Anthropic, OpenAI, and local Ollama. The active model name forms part of the acknowledgement fingerprint. In direct mode, the assembled prompt is sent in one request and the returned JSON is parsed by the shared schema module. In multi-tool mode, the provider chat model can call the Loki, Prometheus, and HTTP-probe tools before returning a verdict, subject to an iteration limit. Both modes return the same normalised fields.'));

  b.push(h3('4.2.4  Prompt Construction and Response Validation'));
  b.push(p('Prompt assembly (agent/llm/prompts.py) serialises the telemetry sections that are available and includes rules that absent optional integrations must not be treated as incidents. The shared parser in agent/llm/schema.py requires a JSON object and an allowed severity, then normalises summary, root-cause, action, and signature fields. Missing text fields become empty strings and additional fields are ignored. This is a structured response contract with severity validation, not a full JSON Schema validator.'));

  b.push(h3('4.2.5  The Verdict-Memory'));
  b.push(p('The acknowledgement feature is implemented across agent/memory.py, api/store.py, the prompt assembler, and the acknowledgement endpoints. Figure 4.2 shows the flow. A verdict signature is combined with the prompt version and model name to create a SHA-256 fingerprint. The operator can acknowledge an ok or warning verdict and optionally set a note and expiry time. Active acknowledgements are included in later prompts as context, but the model call still runs on every heartbeat. The API marks a matching ok or warning verdict as suppressed and the dashboard hides it by default. A changed signature, prompt version, or model produces a different fingerprint. Store and endpoint checks prevent high and critical verdicts from being suppressed.'));
  b.push(blank());
  b.push(image('figures/fig_4_2_llm_classes.png', { w: 6.1, h: 3.25 }));
  b.push(figureCaption('Figure 4.2: Verdict-Memory Fingerprint and Acknowledgement Flow.'));
  b.push(blank());

  b.push(h3('4.2.6  Telemetry Collection Tools'));
  b.push(p('Each telemetry adapter returns either structured data or a structured error. The Loki adapter (agent/tools/loki.py) calls query_range for a defined recent window, in newest-first order, with a configurable limit. The Prometheus adapter issues instant queries for CPU, memory, disk, and HTTP 5xx-rate signals. HTTP probes record status and latency for each configured endpoint. Docker event, diagnostic, and error-log collection runs only when Docker monitoring is enabled.'));

  b.push(h3('4.2.7  The RAG Runbook Service'));
  b.push(p('The runbook service (agent/rag/) reads Markdown files from the configured local directory and indexes them into ChromaDB using local ONNX embeddings. A query retrieves the top-k most similar chunks, formats them into a grounding context, and asks the configured model to answer only from those runbooks with source attribution. Indexing is triggered on demand from the dashboard, and the API runs both indexing and querying off the event loop.'));

  b.push(h3('4.2.8  Threat Detection and CrowdSec Response'));
  b.push(p('Threat detection in agent/tools/threat_response.py does not use an LLM. It counts repeated HTTP 401/403 responses, SSH authentication failures, and rapid connection attempts by source IP, then reports a threat when a configured threshold is crossed. If the operator approves a response, the API builds the CrowdSec ban decision from the recorded threat fields and submits it to the CrowdSec Local API. Without a configured CrowdSec endpoint, the same action is logged as a dry run.'));

  b.push(h3('4.2.9  The API Service and Middleware'));
  b.push(p('The API (api/main.py) is a FastAPI application that serves the dashboard and a JSON REST surface. Four middlewares are registered. An audit middleware records requests, a security-headers middleware applies a content-security policy and standard headers, a rate-limiting middleware enforces per-IP limits, and an authentication middleware requires a valid signed session cookie except for the public health and login endpoints. Login has a stricter route limit. The runbook query, indexing operation, and Loki-backed threat scan execute on worker threads so that blocking integration calls do not stop the event loop.'));

  b.push(h3('4.2.10  Persistence and Retention'));
  b.push(p('Persistence (api/store.py) uses SQLite through aiosqlite and comprises the verdicts and acknowledgements tables described in Section 3.4.1. The schema is created and migrated idempotently on every connection, so an existing database is upgraded in place with the signature and fingerprint columns. Each insert prunes verdict rows older than the configurable retention window, bounding the store’s growth without a separate maintenance job.'));

  b.push(h3('4.2.11  The Dashboard'));
  b.push(p('The dashboard (dashboard/index.html) is a single page served by FastAPI. It displays the current verdict, integration status, agent staleness, detected threats, runbook queries, and recent checks. Root-cause and recommended-action text can be expanded when needed.'));
  b.push(p('For ok and warning verdicts, the page provides mark-as-known and unmark controls, a known tag, and a toggle that reveals acknowledged rows. Before text from the server, model, or logs is inserted into the page, it passes through one HTML-escaping helper. This reduces the cross-site-scripting risk from untrusted log or model content. Figure 4.3 shows the dashboard.'));
  b.push(blank());
  b.push(image('figures/fig_4_3_dashboard.png', { w: 6.1, h: 3.58 }));
  b.push(figureCaption('Figure 4.3: Dashboard Overview Page.'));
  b.push(blank());

  b.push(h3('4.2.12  API Endpoints'));
  b.push(blank());
  const apiColWidths = [2400, 900, 5726];
  const apiRows = [
    ['Endpoint', 'Method', 'Purpose'],
    ['/', 'GET', 'Serve the dashboard (authenticated).'],
    ['/login, /logout', 'GET/POST', 'Session authentication; login is rate-limited to five attempts per minute.'],
    ['/health', 'GET', 'Liveness check (public).'],
    ['/status', 'GET', 'Latest verdict with staleness and memory (fingerprint, acknowledged, suppressed) fields.'],
    ['/alerts', 'GET', 'Recent verdict history with per-row memory fields.'],
    ['/api/config', 'GET', 'Which integrations are configured (booleans only).'],
    ['/api/agent/mode', 'GET', 'Active reasoning mode and model.'],
    ['/api/threats', 'GET', 'Scan recent Loki logs for brute-force and port-scan patterns.'],
    ['/api/threats/apply', 'POST', 'Apply a CrowdSec ban for a detected threat (dry-run without CrowdSec).'],
    ['/api/verdicts/ack', 'POST', 'Acknowledge a verdict condition as a known non-issue.'],
    ['/api/verdicts/unack', 'POST', 'Remove an acknowledgement so the condition re-opens.'],
    ['/api/acks', 'GET', 'List the active acknowledgements.'],
    ['/api/runbooks/query', 'POST', 'Answer a question over the indexed runbooks (RAG).'],
    ['/api/runbooks/index', 'POST', 'Re-index local Markdown runbooks into ChromaDB.'],
  ];
  b.push(buildTable(apiColWidths, apiRows));
  b.push(blank());
  b.push(tableCaption('Table 4.2: API Endpoint Reference.'));

  // 4.3 SECURITY, PERFORMANCE, SCALABILITY
  b.push(h2('4.3  Security, Performance, and Scalability Considerations'));
  b.push(h3('4.3.1  Authentication and Session Management'));
  b.push(p('All non-public endpoints require a session cookie signed with an itsdangerous timestamped serialiser and an environment-provided secret. Sessions expire after twenty-four hours and the authentication middleware checks the cookie on every request. Credential comparison uses hmac.compare_digest to limit timing differences. The cookie is marked HttpOnly and is also marked Secure when the dashboard is served over HTTPS.'));
  b.push(h3('4.3.2  Rate Limiting and Output Hygiene'));
  b.push(p('The slowapi middleware applies a general request limit and a stricter login limit. Dashboard rendering uses a shared escaping helper for server-derived text. The response middleware adds a content-security policy and other headers. The current policy permits inline script and style content because the dashboard is a single HTML file; this weakens the policy and should be removed in a hardened deployment by moving scripts and styles to separate files.'));
  b.push(h3('4.3.3  Auditability'));
  b.push(p('The audit middleware writes one structured JSON line per request with timestamp, client IP, method, route, user, status, and elapsed time. The file is a local operational log. It is not cryptographically protected or tamper-evident, so external log shipping and retention controls are recommended for production use.'));
  b.push(h3('4.3.4  Performance and Responsiveness'));
  b.push(p('The agent and API run as separate processes. API routes that perform blocking model, runbook-indexing, or Loki operations dispatch that work to a worker thread. The default heartbeat is 120 seconds, and one model analysis is performed per heartbeat. This design bounds request frequency, but latency and cost were not measured in the present evaluation.'));
  b.push(h3('4.3.5  Scalability and Degradation'));
  b.push(p('The design targets one host and its co-located workloads; multi-host operation is future work. Each telemetry tool converts a failed request into a structured error, so the next prompt contains less evidence instead of terminating the cycle. A failed model call produces a warning fallback verdict so the failure is recorded.'));
  b.push(h3('4.3.6  Deployment Boundary'));
  b.push(p('The supplied Terraform firewall currently exposes ports 80, 443, 3100, 9090, and 8080 to all source addresses, while Docker Compose publishes the API on port 8080 without a bundled TLS proxy. This is suitable only for a controlled demonstration network. A production deployment should expose only the HTTPS entry point, restrict administration and telemetry ports to trusted networks, set the secure-cookie option, and manage credentials outside the deployment directory.'));

  // 4.4 CHALLENGES
  b.push(h2('4.4  Challenges Encountered'));
  b.push(h3('4.4.1  LLM Output Conformance'));
  b.push(p('A provider response may contain markdown fences, surrounding prose, or an unsupported severity. The single-call mode requests application/json, and the shared parser extracts the outermost JSON object, normalises the expected fields, and checks the severity against the allowed values. A failed parse yields a structured error and a fallback verdict.'));
  b.push(h3('4.4.2  Scope Bounding and False Alarms'));
  b.push(p('The prompt contains explicit scope rules for optional integrations because absent evidence can otherwise be interpreted as a failure. Automated tests confirm that prompt construction includes only configured sections and the required instruction. Live-model false-positive rates were not measured.'));
  b.push(h3('4.4.3  Signature Stability for the Memory'));
  b.push(p('For the verdict memory to be useful, the condition signature must remain stable when volatile telemetry values change. The prompt requests a structured "<source>:<condition>:<resource>" signature at low temperature. If the model omits it, the implementation derives a fallback after removing timestamps, IP addresses, numbers, and hashes.'));
  b.push(h3('4.4.4  Security Defects Corrected During Review'));
  b.push(p('Implementation review identified two defects that were corrected: the rate limiter was configured without its middleware, and server-derived text was inserted into the dashboard without a shared escaping path. Regression tests cover the corrected behaviour. The remaining deployment and CSP limitations are recorded in Section 4.3.'));
  b.push(h3('4.4.5  Loki Query Semantics'));
  b.push(p('An early implementation used Loki\'s instant-query endpoint and produced inconsistent recent-log results. The revised adapter uses a range query over an explicit window in newest-first order. This also gives the threat scanner enough log lines to evaluate its configured thresholds.'));

  return b;
}

module.exports = { chapter4 };
