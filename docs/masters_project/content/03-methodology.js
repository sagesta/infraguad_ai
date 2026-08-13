const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable, image, figureCaption, tableCaption } = require('../helpers');

function chapter3() {
  const b = [];

  b.push(chapterLabel('CHAPTER THREE: METHODOLOGY AND SYSTEM DESIGN'));
  b.push(blank());

  // 3.1 PROJECT METHODOLOGY
  b.push(h2('3.1  Project Methodology'));
  b.push(p('The project uses an iterative design-science method. Design-science research is appropriate because the work produces and evaluates a software artefact intended to address a defined operational problem (Hevner et al., 2004). Short implementation cycles were used within that build-and-evaluate process so that requirements, code, tests, and documentation could be revised together.'));

  b.push(h3('3.1.1  Methodological Phases'));
  b.push(p('The work was organised into six phases. The phases overlapped where test results or code review required an earlier decision to be revised.'));
  b.push(num('Problem identification. Reviewed observability, SRE, AIOps, incident-analysis, RAG, and agent research, then defined the narrow problem of first-pass telemetry interpretation for a small team.'));
  b.push(num('Objective definition. Converted the problem into five implementation and evaluation objectives.'));
  b.push(num('Design and development. Implemented telemetry adapters, the reasoning workflow, provider abstraction, runbook retrieval, threat handling, persistence, API, dashboard, and acknowledgement memory.'));
  b.push(num('Demonstration. Exercised the main workflow paths with mocked upstream services and controlled test fixtures.'));
  b.push(num('Evaluation. Ran the automated test and coverage suite and compared the displayed duplicate count before and after an acknowledgement. A usability instrument was prepared but not administered.'));
  b.push(num('Communication. Updated the report, diagrams, references, and appendices so that they describe the implemented system and measured evidence.'));

  b.push(h3('3.1.2  Justification for the Methodology Choice'));
  b.push(p('A fixed sequential method was not selected because several requirements depended on implementation findings, especially output parsing, acknowledgement matching, and middleware order. A design-science structure retains a clear link between the identified problem, the artefact, and the evaluation while allowing those details to be revised during development.'));

  b.push(h3('3.1.3  Tools Supporting the Methodology'));
  b.push(p('The Git repository contains the source code, infrastructure definitions, tests, and report sources. Two GitHub Actions workflows are included: pull requests run the test suite, while pushes to the main branch run tests before the container build and deployment steps.'));

  // 3.2 REQUIREMENTS ANALYSIS
  b.push(h2('3.2  Requirements Analysis'));
  b.push(p('The operational setting and project scope were converted into functional and non-functional requirements. Each requirement was checked against the repository and marked Must or Should according to whether it formed part of the core heartbeat, operator control, or optional integration path. Features outside the delivered boundary are listed as future work in Section 1.4.2.'));

  b.push(h3('3.2.1  Functional Requirements'));
  b.push(blank());
  const fnColWidths = [800, 2400, 4000, 1826];
  const fnRows = [
    ['ID', 'Requirement', 'Description', 'Priority'],
    ['FR-01', 'Telemetry Collection', 'The system shall collect logs (Loki), metrics (Prometheus), endpoint health (HTTP probes), and optional container state (Docker Engine API) on a configurable heartbeat interval.', 'Must'],
    ['FR-02', 'Structured Verdict Generation', 'The system shall send collected context to the configured LLM provider and request a verdict containing severity, summary, root cause, recommended action, and signature.', 'Must'],
    ['FR-03', 'Severity Classification', 'Each verdict shall be classified into one of four severities: ok, warning, high, or critical.', 'Must'],
    ['FR-04', 'Dual Reasoning Modes', 'The system shall support a single-call Gemini mode and a LangChain multi-tool agent mode, selectable by configuration, recording which mode produced each verdict.', 'Must'],
    ['FR-05', 'Notification', 'The system shall dispatch a push notification via ntfy.sh for verdicts of high or critical severity.', 'Must'],
    ['FR-06', 'Verdict Persistence and Retention', 'Verdicts shall be persisted to SQLite and automatically pruned after a configurable retention window.', 'Must'],
    ['FR-07', 'Verdict Memory (Acknowledgement)', 'The system shall fingerprint each verdict on its condition signature plus ruleset version and allow an operator to acknowledge a low-risk condition so that a matching verdict is marked suppressed.', 'Must'],
    ['FR-08', 'Memory Matching', 'A changed condition signature, prompt version, or model shall produce a different fingerprint; acknowledgements may also expire after a configurable time-to-live.', 'Must'],
    ['FR-09', 'Severity Safeguard', 'High- and critical-severity verdicts shall never be suppressed by an acknowledgement.', 'Must'],
    ['FR-10', 'Threat Detection', 'The system shall scan recent logs for HTTP/SSH brute-force and port-scan patterns and surface detected threats with their source IPs.', 'Must'],
    ['FR-11', 'Operator-Approved Threat Response', 'On explicit operator approval, the system shall build and apply a CrowdSec ban for a detected threat, operating in dry-run mode when CrowdSec is unconfigured.', 'Should'],
    ['FR-12', 'Runbook Indexing', 'The system shall index Markdown runbooks from a configured local directory into a ChromaDB vector store on demand.', 'Must'],
    ['FR-13', 'Runbook Query (RAG)', 'The system shall answer operator questions over the indexed runbooks, returning a grounded answer and source citations.', 'Must'],
    ['FR-14', 'Operations Dashboard', 'The system shall provide a web dashboard exposing current status, integration configuration, check history, the threat panel, and the runbook assistant.', 'Must'],
    ['FR-15', 'Integration Status', 'The system shall report which integrations are configured, exposing booleans only and never secret values.', 'Should'],
  ];
  b.push(buildTable(fnColWidths, fnRows));
  b.push(blank());
  b.push(tableCaption('Table 3.1: Functional Requirements of InfraGuard AI.'));

  b.push(h3('3.2.2  Non-Functional Requirements'));
  b.push(blank());
  const nfColWidths = [800, 2200, 4200, 1826];
  const nfRows = [
    ['ID', 'Quality Attribute', 'Requirement', 'Target'],
    ['NFR-01', 'Cost Control', 'The heartbeat interval and prompt size shall be configurable so provider usage can be bounded.', 'One analysis request per heartbeat'],
    ['NFR-02', 'Grounding Controls', 'The prompt shall include only configured evidence sections and shall instruct the model not to treat absent integrations as failures.', 'Covered by prompt-construction tests'],
    ['NFR-03', 'Responsiveness', 'Blocking LLM, runbook-indexing, and Loki operations in the API shall run off the event loop.', 'No direct blocking call in route coroutine'],
    ['NFR-04', 'Authentication', 'All routes other than /health and /login shall require a valid signed session cookie.', '24-hour maximum age'],
    ['NFR-05', 'Rate Limiting', 'The API shall enforce request limits, with a stricter limit on the login route.', '60/min; 5/min on login'],
    ['NFR-06', 'Output Hygiene', 'Server-derived text rendered in the dashboard shall be HTML-escaped and response security headers shall be applied.', 'Escaping and headers covered by tests'],
    ['NFR-07', 'Auditability', 'Each request shall be logged with timestamp, IP, route, method, user, status, and latency.', 'Structured local request log'],
    ['NFR-08', 'Portability', 'The API and agent shall deploy through Docker Compose on one Linux host.', 'Single-host composition'],
    ['NFR-09', 'Maintainability', 'The backend shall have an automated suite with measured line coverage.', 'Coverage reported, not used as a sole quality measure'],
    ['NFR-10', 'Data Minimisation', 'Only selected telemetry sections shall be included in the prompt sent to the configured LLM provider.', 'No full observability-store export'],
    ['NFR-11', 'Storage Retention', 'Verdict storage shall be bounded by automatic retention pruning.', 'Default 30 days, configurable'],
    ['NFR-12', 'Signature Stability', 'Fallback signature derivation shall remove volatile IP, hash, and numeric tokens.', 'Deterministic tests'],
  ];
  b.push(buildTable(nfColWidths, nfRows));
  b.push(blank());
  b.push(tableCaption('Table 3.2: Non-Functional Requirements of InfraGuard AI.'));

  b.push(h3('3.2.3  Actors and Use Cases'));
  b.push(p('The use-case model has three actors. The Operator is responsible for the monitored infrastructure. The InfraGuard Agent runs the heartbeat without direct user input, and the configured LLM Provider participates as an external service. Figure 3.4 shows their interactions.'));
  b.push(bullet('UC-01: View the current status and verdict (Operator → System).'));
  b.push(bullet('UC-02: Inspect the root cause and recommended action of a verdict (Operator → System).'));
  b.push(bullet('UC-03: Acknowledge a verdict as a known non-issue (Operator → System).'));
  b.push(bullet('UC-04: Un-acknowledge a condition so it re-opens (Operator → System).'));
  b.push(bullet('UC-05: Review detected threats (Operator → System).'));
  b.push(bullet('UC-06: Apply a CrowdSec ban for a detected threat (Operator → System).'));
  b.push(bullet('UC-07: Ask the runbook assistant a question (Operator → System).'));
  b.push(bullet('UC-08: Re-index local Markdown runbooks (Operator → System).'));
  b.push(bullet('UC-09: Generate a verdict on a heartbeat, consulting the LLM provider (Agent → LLM Provider).'));
  b.push(bullet('UC-10: Dispatch a notification on a high or critical verdict (Agent → Operator).'));

  // 3.3 ARCHITECTURE
  b.push(h2('3.3  System Architecture'));
  b.push(p('InfraGuard AI uses two processes: an agent process that runs the reasoning heartbeat and an API process that serves the dashboard and REST surface. Both use the same SQLite database. Blocking API work is moved to worker threads so that long-running integration calls do not block the event loop. Figure 3.1 shows the main components.'));

  b.push(h3('3.3.1  Architectural Style'));
  b.push(p('The single-host architecture separates collection, verdict generation, and memory logic from adapters for Loki, Prometheus, HTTP probes, Docker, and the LLM provider. Each adapter implements a small interface. As a result, a source can be omitted or replaced without changing the rest of the workflow, and its behaviour can be tested in isolation.'));

  b.push(h3('3.3.2  Components'));
  b.push(num('Agent (Heartbeat). A long-running asyncio process that, on each interval, fetches operator acknowledgements, collects telemetry, invokes the LangGraph reasoning loop, persists the verdict, and dispatches notifications. Implemented in agent/main.py and agent/orchestrator.py.'));
  b.push(num('FastAPI Service. Hosts the dashboard and the REST API (status, alerts, configuration, threats, runbooks, and acknowledgement endpoints) behind authentication, rate-limiting, security-header, and audit middleware. Implemented in api/main.py.'));
  b.push(num('Reasoning Substrate. A LangGraph state machine implementing the collect-analyse-decide-notify loop, with two interchangeable analysis modes: a single structured Gemini call and a LangChain multi-tool agent.'));
  b.push(num('LLM Client. A provider-neutral layer using the direct Gemini Developer API by default, with Anthropic, OpenAI, and local Ollama alternatives.'));
  b.push(num('Verdict-Memory. The fingerprinting and acknowledgement subsystem (agent/memory.py and the acknowledgements table) that suppresses already-triaged conditions and feeds them back into the prompt as known conditions.'));
  b.push(num('RAG Service. The local Markdown runbook ingestion and retrieval pipeline over ChromaDB with local ONNX embeddings.'));
  b.push(num('Threat Subsystem. A deterministic detector that scans recent logs for attack patterns and an operator-approved CrowdSec adapter.'));
  b.push(num('SQLite Store. The persistence layer for verdicts and acknowledgements, with automatic retention pruning.'));
  b.push(num('Dashboard. A single self-contained HTML, CSS, and JavaScript page served as a static asset by FastAPI and communicating over JSON.'));
  b.push(num('External Services. The selected model API, ntfy.sh for notifications, and an optional CrowdSec Local API for threat response. Gemini, Anthropic, and OpenAI are supported; Ollama can keep inference local.'));

  b.push(h3('3.3.3  Communication Patterns'));
  b.push(p('On each heartbeat, the agent queries the Loki and Prometheus HTTP APIs, runs the configured HTTP probes, and may read the Docker Engine API. It stores verdicts in the SQLite database and reads acknowledgements from the same database used by the API. The dashboard exchanges JSON with the API and authenticates with a session cookie. HTTPS termination is supplied by the deployment environment.'));

  b.push(h3('3.3.4  High-Level Architecture'));
  b.push(p('Figure 3.1 presents the high-level architecture. The agent and API share the SQLite volume. ChromaDB is mounted only in the API container for runbook retrieval. The agent reads configured telemetry sources and calls the selected LLM provider. It calls ntfy.sh for high and critical verdicts. The API calls the optional CrowdSec Local API only after an operator request.'));
  b.push(blank());
  b.push(image('figures/fig_3_1_architecture.png', { w: 6.1, h: 3.82 }));
  b.push(figureCaption('Figure 3.1: InfraGuard AI High-Level System Architecture.'));
  b.push(blank());

  b.push(h3('3.3.5  Deployment Topology'));
  b.push(p('Figure 3.2 depicts the deployment topology. Docker Compose starts the agent, API, and optional Ollama service on a Google Compute Engine virtual machine provisioned by Terraform. The agent and API share the SQLite volume; the API uses the ChromaDB volume and a read-only mount of the local runbooks directory. Loki, Prometheus, monitored endpoints, a selected cloud provider when configured, ntfy.sh, and CrowdSec remain external dependencies.'));
  b.push(blank());
  b.push(image('figures/fig_3_2_topology.png', { w: 6.1, h: 3.82 }));
  b.push(figureCaption('Figure 3.2: Single-Host Deployment Topology.'));
  b.push(blank());

  b.push(h3('3.3.6  Heartbeat Verdict Pipeline'));
  b.push(p('Figure 3.3 traces one heartbeat. The agent fetches active acknowledgements, collects configured telemetry, constructs the prompt, calls the selected model, parses the verdict, computes the signature and fingerprint, and persists the result. A high or critical verdict is routed to notification. The acknowledgement does not skip analysis. After persistence, a matching ok or warning verdict is marked suppressed by the API and hidden by default in the dashboard.'));
  b.push(blank());
  b.push(image('figures/fig_3_3_remediation_flow.png', { w: 6.1, h: 3.58 }));
  b.push(figureCaption('Figure 3.3: Heartbeat Verdict Pipeline: Collect, Analyse, Store, Present.'));
  b.push(blank());

  // 3.4 SYSTEM DESIGN
  b.push(h2('3.4  System Design'));
  b.push(p('The detailed design covers the database schema, the normal heartbeat sequence, acknowledgement matching, the reasoning state machine, and runbook indexing.'));

  b.push(h3('3.4.1  Database Design (Entity-Relationship Model)'));
  b.push(p('SQLite stores operational state in two relational tables. ChromaDB stores runbook embeddings, and an append-only file receives API audit events. Figure 3.6 shows the entity-relationship model; the text below lists the fields.'));
  b.push(h4('Entity: verdicts'));
  b.push(p('Columns: id (PK, AUTOINCREMENT), created_at (TEXT, UTC ISO-8601), severity (TEXT), summary (TEXT), payload (TEXT, JSON of the full verdict and extras), signature (TEXT), fingerprint (TEXT). Each heartbeat appends one row; rows older than the retention window are pruned on insert.'));
  b.push(h4('Entity: acknowledgements'));
  b.push(p('Columns: fingerprint (PK, TEXT), signature (TEXT), severity (TEXT), summary (TEXT), note (TEXT), acked_by (TEXT), created_at (TEXT), expires_at (TEXT, nullable). One row per acknowledged condition; an acknowledgement is active while expires_at is null or in the future.'));
  b.push(p('Verdicts and acknowledgements are matched by fingerprint. Several verdict rows may share a fingerprint when the same condition recurs, while each fingerprint can have at most one active acknowledgement. A matching verdict is marked acknowledged. It is marked suppressed only when its severity is ok or warning.'));

  b.push(h3('3.4.2  Use-Case Model'));
  b.push(p('Figure 3.4 presents the use-case diagram. The Operator interacts with the system through the dashboard for status review, verdict acknowledgement, threat review and response, and runbook queries. The Agent interacts autonomously with the LLM Provider to generate verdicts and with the Operator through notifications.'));
  b.push(blank());
  b.push(image('figures/fig_3_4_usecase.png', { w: 6.1, h: 4.27 }));
  b.push(figureCaption('Figure 3.4: Use-Case Diagram: Operator and Agent.'));
  b.push(blank());

  b.push(h3('3.4.3  Sequence Diagram: One Heartbeat Cycle'));
  b.push(p('Figure 3.5 shows one heartbeat. The agent first loads active acknowledgements and collects telemetry from Loki, Prometheus, and the HTTP probes. It adds known conditions to the prompt, calls the LLM provider, checks the structured verdict, and computes the signature and fingerprint. The verdict is then stored. High or critical severity triggers the notification path. On a separate refresh interval, the dashboard reads the latest verdict and history from the API.'));
  b.push(blank());
  b.push(image('figures/fig_3_5_sequence.png', { w: 6.1, h: 4.07 }));
  b.push(figureCaption('Figure 3.5: Sequence Diagram: One Heartbeat Cycle.'));
  b.push(blank());

  b.push(h3('3.4.4  Entity-Relationship Model'));
  b.push(p('Figure 3.6 visualises the two-table schema described above, together with the by-fingerprint relationship between verdicts and acknowledgements and the external ChromaDB and audit-log stores.'));
  b.push(blank());
  b.push(image('figures/fig_3_6_erd.png', { w: 6.1, h: 3.82 }));
  b.push(figureCaption('Figure 3.6: Entity-Relationship Diagram of the Verdict and Acknowledgement Schema.'));
  b.push(blank());

  b.push(h3('3.4.5  Verdict-Memory Design'));
  b.push(p('The acknowledgement memory combines the condition signature, prompt version, and model in a SHA-256 fingerprint: fingerprint = SHA-256(signature | prompt_version | model). The model is asked to return a short signature such as "prometheus:disk-low:/". If it does not, the fallback removes IP addresses, hashes, and numbers from the root-cause or summary text before creating a slug. An operator acknowledgement stores the fingerprint with an optional note and expiry time. A changed signature, prompt version, or model produces a new fingerprint that does not match the previous acknowledgement. The previous database row remains until it expires or is removed. Matching ok and warning verdicts can be suppressed in the API and dashboard; high and critical verdicts cannot.'));

  b.push(h3('3.4.6  State Machine: LangGraph Reasoning Agent'));
  b.push(p('Figure 3.7 depicts the LangGraph state machine that governs the reasoning agent. Four nodes, collect_data, analyze, decide_action, and notify, are used on each heartbeat. The graph begins at collect_data, proceeds to analyze and decide_action, and routes high- and critical-severity verdicts to notify. Other verdicts end without notification. When local Docker monitoring is enabled, decide_action can also gather container diagnostics for high- and critical-severity verdicts.'));
  b.push(blank());
  b.push(image('figures/fig_3_7_state_machine.png', { w: 6.1, h: 3.01 }));
  b.push(figureCaption('Figure 3.7: State Machine of the LangGraph Reasoning Agent.'));
  b.push(blank());

  b.push(h3('3.4.7  Workflow: Runbook RAG Indexing'));
  b.push(p('Runbook indexing runs on demand when the operator uses POST /api/runbooks/index. The indexer reads Markdown files from the configured runbook directory and retains filenames and subdirectories as source metadata. It chunks the text, creates local embeddings, and writes the chunks to ChromaDB. For a query, the retriever returns the top-k matching chunks. The configured model receives those chunks with the operator\'s question, and the API returns the answer with the retrieved source titles.'));

  // 3.5 TOOLS AND TECHNOLOGIES
  b.push(h2('3.5  Tools and Technologies Used'));
  b.push(p('The implementation uses the tools listed below, grouped by layer. Table 3.3 gives the telemetry sources and collection modules.'));
  b.push(h3('3.5.1  Backend and Orchestration'));
  b.push(bullet('Language and runtime: Python 3.11+ with asyncio.'));
  b.push(bullet('Web/API framework: FastAPI with Uvicorn.'));
  b.push(bullet('LLM orchestration: LangGraph and LangChain.'));
  b.push(bullet('LLM providers: direct Gemini Developer API by default, with Anthropic, OpenAI, and local Ollama alternatives.'));
  b.push(bullet('Vector store: ChromaDB with local ONNX text embeddings.'));
  b.push(bullet('Persistence: SQLite via aiosqlite.'));
  b.push(bullet('HTTP client: httpx; runbook source: local Markdown files under RUNBOOKS_DIR.'));
  b.push(h3('3.5.2  Security and Deployment'));
  b.push(bullet('Sessions: itsdangerous signed cookies; rate limiting: slowapi; security headers and CSP via custom middleware.'));
  b.push(bullet('Threat response: CrowdSec Local API.'));
  b.push(bullet('Notifications: ntfy.sh.'));
  b.push(bullet('Packaging and deployment: Docker and Docker Compose; Terraform for Google Compute Engine; GitHub Actions for CI.'));
  b.push(bullet('Frontend: a single self-contained HTML/CSS/JavaScript dashboard served by FastAPI.'));

  b.push(h3('3.5.3  Telemetry Sources'));
  b.push(p('Table 3.3 enumerates the telemetry sources and the modules that collect them.'));
  b.push(blank());
  const telColWidths = [1500, 2200, 2400, 2926];
  const telRows = [
    ['Source', 'Collection Module', 'Signal', 'Notes'],
    ['Logs', 'agent/tools/loki.py', 'Recent log lines', 'Loki query_range, newest-first, configurable window'],
    ['Metrics', 'agent/tools/prometheus.py', 'CPU, memory, disk, HTTP 5xx ratio', 'Prometheus instant queries'],
    ['Endpoint health', 'agent/tools/http_probe.py', 'Status code and latency', 'Comma-separated PROBE_URLS'],
    ['Container state', 'agent/tools/docker_api.py, docker_events.py', 'Events, stats, health, logs', 'Optional (ENABLE_DOCKER_MONITORING=1)'],
    ['Threats', 'agent/tools/threat_response.py', 'Brute-force / port-scan patterns', 'Deterministic regex over recent logs'],
    ['Runbooks', 'agent/rag/local_runbooks_loader.py', 'Markdown runbook documents', 'Local, read-only RAG corpus source'],
  ];
  b.push(buildTable(telColWidths, telRows));
  b.push(blank());
  b.push(tableCaption('Table 3.3: Telemetry Sources and Collection Tools.'));

  return b;
}

module.exports = { chapter3 };
