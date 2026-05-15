const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable, image } = require('../helpers');

function chapter3() {
  const b = [];

  b.push(chapterLabel('CHAPTER THREE'));
  b.push(pCenter('METHODOLOGY AND SYSTEM DESIGN'));
  b.push(blank());

  // 3.1 PROJECT METHODOLOGY
  b.push(h2('3.1  Project Methodology'));
  b.push(p('The methodology adopted for this project is a hybrid Agile–DevSecOps approach with embedded design science research practice. The choice is justified by the nature of the deliverable: the project produces both an operational software artefact (the InfraGuard Pro reference implementation) and an empirical research contribution (the quantitative evaluation of autonomous remediation across a 150-finding benchmark). Pure Agile, while excellent for iterative engineering, lacks the explicit epistemic discipline required for academic research; pure design science research, while academically defensible, does not naturally accommodate the rapid iteration that LLM-driven systems demand. The hybrid combines the structured artefact-evaluation cycle of design science research (Hevner et al., 2004) with the two-week sprint cadence, retrospective discipline, and continuous deployment of Agile DevSecOps.'));

  b.push(h3('3.1.1  Methodological Phases'));
  b.push(p('The work was executed across six methodological phases, each with explicit entry criteria, deliverables, and exit criteria. The phases overlap in the iterative sense — multiple phases were active during any given sprint — but the formal ordering provides traceability for the academic record.'));
  b.push(num('Phase 1 — Problem Identification and Motivation. Reviewed industry incident reports, conducted informal interviews with five DevSecOps practitioners across Nigerian and African digital enterprises, and confirmed that detection-to-remediation latency was the dominant pain point. Deliverable: the problem statement codified in Chapter One.'));
  b.push(num('Phase 2 — Objectives Definition. Translated the problem statement into five measurable objectives, each tied to a quantitative or qualitative evaluation criterion. Deliverable: the objectives schedule in Section 1.3.'));
  b.push(num('Phase 3 — Design and Development. Conducted ten sprints of two weeks each, building the LLM provider abstraction, the SARIF ingestion pipeline, the policy engine, the satellite agent, the Git provider integrations, the dashboard, and the closed-loop validation hooks. Each sprint produced demonstrable software increments deployed to a staging environment representative of the LivWell topology.'));
  b.push(num('Phase 4 — Demonstration. Deployed the integrated system against a controlled multi-container test environment seeded with both real-world vulnerabilities harvested from public datasets and synthetic injections designed to exercise edge cases. Deliverable: the demonstration scripts in Appendix B and the test environment configuration in Appendix C.'));
  b.push(num('Phase 5 — Evaluation. Ran the 150-finding benchmark across each of the three policy modes and each of the five LLM providers, capturing accuracy, latency, cost, regression rate, and operator-trust outcomes. Deliverable: the empirical results presented in Chapter Five.'));
  b.push(num('Phase 6 — Communication. Authored the present report, prepared the open-source repository for public release, and prepared the seminar presentation. Deliverable: the present project document and the associated public artefact.'));

  b.push(h3('3.1.2  Justification for the Methodology Choice'));
  b.push(p('Three alternative methodologies were considered and rejected. Waterfall was rejected because the LLM-provider landscape evolves on a quarterly timescale; locking the design before any code is written would have produced a system already obsolete at delivery. Pure Scrum was rejected because Scrum’s deliberate silence on the epistemic structure of the work would have weakened the research defensibility of the final report. The Spiral model was considered but offered no advantages over the hybrid Agile–design-science model adopted, while imposing additional ceremony. The hybrid model selected captures the iterative empiricism of modern AI engineering while preserving the artefact-evaluation–reflection cycle that makes the work academically defensible.'));

  b.push(h3('3.1.3  Tools Supporting the Methodology'));
  b.push(p('Sprint planning and tracking were conducted in GitHub Projects with a Kanban board mapped to the six-phase model. The repository itself served as the single source of truth for all artefacts: source code, infrastructure-as-code, evaluation datasets, benchmark scripts, and the LaTeX/Markdown drafts of report chapters. Continuous integration was performed by GitHub Actions; deployments to the staging environment were triggered automatically on every merge to the main branch.'));

  // 3.2 REQUIREMENTS ANALYSIS
  b.push(h2('3.2  Requirements Analysis'));
  b.push(p('The requirements analysis was conducted in two stages. First, the operational pain points surfaced in Phase 1 interviews were translated into a candidate user-story backlog. Second, each user story was decomposed into functional and non-functional requirements through the MoSCoW prioritisation method (Must, Should, Could, Won’t). The Must and Should requirements are tabulated below; Could requirements were tracked in the backlog but are out-of-scope for the present deliverable, while Won’t requirements are documented in Section 1.4.2.'));

  b.push(h3('3.2.1  Functional Requirements'));
  b.push(blank());
  const fnColWidths = [800, 2400, 4000, 1826];
  const fnHeaders = ['ID', 'Requirement', 'Description', 'Priority'];
  const fnRows = [
    fnHeaders,
    ['FR-01', 'SARIF Ingestion', 'The system shall ingest SARIF 2.1.0 output from at least six distinct scanner classes (SAST, SCA, container, IaC, secret, dependency) over an HTTP POST endpoint or by polling a configured CI/CD artefact store.', 'Must'],
    ['FR-02', 'Finding Normalisation', 'Ingested findings shall be normalised into a unified internal representation including rule identifier, CWE, CVSS, source location, optional fix suggestion, and provenance metadata.', 'Must'],
    ['FR-03', 'LLM Provider Abstraction', 'The system shall support runtime selection among at least five LLM providers (Vertex AI, OpenAI, Anthropic, Kimi, Ollama) without restart.', 'Must'],
    ['FR-04', 'Patch Generation', 'For each ingested finding the system shall produce a structured patch proposal containing a diff, a confidence score, a citation chain, and a policy classification.', 'Must'],
    ['FR-05', 'Policy Classification', 'Each patch shall be classified by the policy engine into one of three execution modes: recommend-only, human-approval-required, autonomous-low-risk.', 'Must'],
    ['FR-06', 'Git Provider Pull Request', 'Approved patches shall be applied through a pull request created via the GitHub or GitLab API with the patch diff, the LLM reasoning, and the evidence chain in the PR body.', 'Must'],
    ['FR-07', 'Closed-Loop Validation', 'After deployment of a patched artefact the system shall re-run the originating scanner against the patched artefact and watch runtime telemetry for regressions over a configurable observation window.', 'Must'],
    ['FR-08', 'Multi-Server Satellite Topology', 'The system shall support an arbitrary number of remote satellite agents, each registering with the central control plane and reporting telemetry on a configurable heartbeat interval.', 'Must'],
    ['FR-09', 'RAG Runbook Indexing', 'The system shall index runbooks from Notion, local Markdown files, uploaded artefacts, and historical verdicts into a ChromaDB vector store and retrieve the top-k most similar items on every patch generation.', 'Must'],
    ['FR-10', 'Audit Logging', 'Every action — ingestion, retrieval, LLM invocation, patch proposal, policy decision, pull-request creation, merge, post-deployment validation — shall be recorded in a tamper-evident append-only audit log.', 'Must'],
    ['FR-11', 'Operations Dashboard', 'The system shall provide a web-based dashboard exposing the fleet overview, server detail, container detail, verdicts feed, remediation queue, runbook browser, and LLM configuration panels.', 'Must'],
    ['FR-12', 'Notification Routing', 'Verdicts and remediation events of configurable severity shall be dispatched to ntfy.sh topics, Slack webhooks, and SMTP recipients according to per-server routing rules.', 'Should'],
    ['FR-13', 'Container Operations', 'Authorised operators shall be able to restart, stop, or inspect logs of any container on any registered satellite, with every action recorded in the audit log.', 'Should'],
    ['FR-14', 'On-Demand Diagnosis', 'Operators shall be able to trigger an immediate diagnosis or remediation cycle for a specific container or finding without waiting for the next heartbeat.', 'Should'],
    ['FR-15', 'Fix Outcome Tracking', 'For every applied patch the system shall record whether the post-deployment validation succeeded or failed and shall index the outcome into the RAG corpus to inform future generations.', 'Should'],
  ];
  b.push(buildTable(fnColWidths, fnRows));
  b.push(blank());
  b.push(p('Table 3.1: Functional Requirements of InfraGuard Pro.', { align: require('docx').AlignmentType.CENTER }));

  b.push(h3('3.2.2  Non-Functional Requirements'));
  b.push(blank());
  const nfColWidths = [800, 2200, 4200, 1826];
  const nfHeaders = ['ID', 'Quality Attribute', 'Requirement', 'Target'];
  const nfRows = [
    nfHeaders,
    ['NFR-01', 'Performance — Ingestion', 'The system shall ingest and normalise a SARIF document with up to 1,000 findings within a bounded latency.', '≤ 5 seconds p95'],
    ['NFR-02', 'Performance — End-to-End MTTR', 'For autonomous-mode low-risk findings the median end-to-end time from ingestion to merged pull request shall not exceed a target threshold.', '≤ 10 minutes'],
    ['NFR-03', 'Scalability — Satellites', 'The control plane shall support concurrent operation of at least fifty satellite agents without saturation.', '≥ 50 satellites'],
    ['NFR-04', 'Reliability — Satellite Connectivity', 'Satellites shall buffer telemetry locally and replay on reconnection following a central-plane outage.', '≥ 1 hour buffer'],
    ['NFR-05', 'Security — Authentication', 'All API endpoints (other than /login and /health) shall require a valid session cookie with HMAC-signed serialisation and a maximum lifetime.', '24-hour max age'],
    ['NFR-06', 'Security — Audit Integrity', 'The audit log shall be append-only, with each entry chained to the previous entry by SHA-256 hash.', 'Tamper-evident'],
    ['NFR-07', 'Privacy — LLM Data Handling', 'Sensitive payloads (secrets, customer data) shall be redacted from LLM prompts; the system shall support a fully on-premises LLM via Ollama with no external network egress.', 'On-prem option'],
    ['NFR-08', 'Cost — LLM Spend', 'Per-finding LLM cost shall remain bounded across providers, with the option to fall back to a cheaper provider on cost-budget exhaustion.', '≤ USD 0.05'],
    ['NFR-09', 'Usability — Dashboard Time-to-Insight', 'A new operator shall be able to locate the highest-severity unresolved finding from the dashboard home in three clicks or fewer.', '≤ 3 clicks'],
    ['NFR-10', 'Portability — Self-Hosting', 'The complete system shall deploy via Docker Compose on a single commodity Linux host with no managed-service dependencies.', 'Single-host install'],
    ['NFR-11', 'Maintainability — Test Coverage', 'Backend unit and integration tests shall maintain a minimum line coverage threshold.', '≥ 80% coverage'],
    ['NFR-12', 'Compliance — Audit Retention', 'The audit log shall be retained for a configurable period, default one year, to satisfy regulatory inspection.', '≥ 365 days'],
  ];
  b.push(buildTable(nfColWidths, nfRows));
  b.push(blank());
  b.push(p('Table 3.2: Non-Functional Requirements of InfraGuard Pro.', { align: require('docx').AlignmentType.CENTER }));

  b.push(h3('3.2.3  Actors and Use Cases'));
  b.push(p('Three primary actors interact with the system: the DevSecOps Operator, the Developer, and the CI/CD Pipeline. A fourth actor, the LLM Provider, participates as an external system. The principal use cases are enumerated below and depicted in Figure 3.4.'));
  b.push(bullet('UC-01: Ingest scanner output (Pipeline → System).'));
  b.push(bullet('UC-02: Review the verdicts feed (Operator → System).'));
  b.push(bullet('UC-03: Approve a human-approval-required patch (Operator → System).'));
  b.push(bullet('UC-04: Switch active LLM provider (Operator → System).'));
  b.push(bullet('UC-05: Receive a pull request notification (Developer ← System).'));
  b.push(bullet('UC-06: Trigger on-demand diagnosis (Operator → System).'));
  b.push(bullet('UC-07: Inspect post-deployment validation outcome (Operator → System).'));
  b.push(bullet('UC-08: Roll back a failed patch (Operator → System).'));
  b.push(bullet('UC-09: Search runbooks (Operator → System).'));
  b.push(bullet('UC-10: Apply CrowdSec ban to all satellites (Operator → System).'));

  // 3.3 ARCHITECTURE
  b.push(h2('3.3  System Architecture'));
  b.push(p('InfraGuard Pro is architected as a distributed system comprising a central control plane and an arbitrary number of remote satellite agents. The control plane aggregates state and orchestrates reasoning; the satellites collect local telemetry and execute approved remote actions. Communication between the two is exclusively over authenticated HTTPS using token-based mutual authentication. The high-level architecture is shown in Figure 3.1 and elaborated component-by-component below.'));

  b.push(h3('3.3.1  Architectural Style'));
  b.push(p('The architecture follows a hub-and-spoke pattern with the central control plane at the hub. Within the control plane the architecture is hexagonal (ports-and-adapters): the domain logic of finding ingestion, policy classification, patch generation, and audit recording is isolated behind well-defined interfaces from the concrete adapters that bind to specific scanners, LLM providers, Git providers, and telemetry stores. This isolation is what makes the LLM provider abstraction practical and what permits new scanners to be added by writing only an adapter, not by modifying the core domain.'));

  b.push(h3('3.3.2  Central Control Plane Components'));
  b.push(num('FastAPI Service. Hosts the public REST API for the dashboard, the satellite registration and heartbeat endpoints, the SARIF ingestion endpoint, the on-demand diagnosis endpoint, and the LLM configuration endpoint. Implemented in api/main.py.'));
  b.push(num('Reasoning Agent. A LangGraph state machine implementing the four-phase Collect-Analyse-Decide-Notify loop with an additional Remediate phase. Hosted in a long-running asyncio task started by agent/main.py.'));
  b.push(num('Remediation Engine. The principal new module introduced by this project. Consumes normalised findings, invokes the LLM provider through the abstraction layer, retrieves grounding evidence via the RAG service, classifies the resulting patch via the policy engine, opens a pull request via the Git provider adapter, and triggers post-deployment validation.'));
  b.push(num('LLM Provider Abstraction. A pluggable provider registry with concrete implementations for Vertex AI, OpenAI, Anthropic, Kimi, Ollama, and LM Studio. All providers expose a uniform async reason(context) → Verdict interface.'));
  b.push(num('RAG Service. Wraps the ChromaDB vector store and exposes index, query, and re-index operations across the four configured retrieval sources.'));
  b.push(num('Policy Engine. A rule-based classifier that scores each generated patch on dimensions of LLM confidence, CVE severity, blast radius (number of files affected), and historical fix-outcome track record, and routes the patch to one of the three execution modes.'));
  b.push(num('Audit Service. An append-only logging service with SHA-256 hash chaining for tamper-evidence, persisting to PostgreSQL.'));
  b.push(num('Dashboard. A SvelteKit application served as static assets behind FastAPI, communicating with the API over JSON.'));
  b.push(num('Traceway Subsystem. The OpenTelemetry-native observability stack, comprising the Traceway ingest service and a ClickHouse store for telemetry.'));
  b.push(num('Notification Dispatcher. A multi-channel dispatcher delivering verdict and remediation events to ntfy.sh topics, Slack webhooks, and SMTP recipients.'));
  b.push(num('PostgreSQL Store. The relational store for verdicts, remediations, audit entries, satellites, server metadata, runbooks, and user accounts.'));

  b.push(h3('3.3.3  Satellite Agent Components'));
  b.push(p('Each satellite agent is a single Docker container that bundles the following responsibilities into a minimal Python process: local Prometheus metric scraping, local Loki log shipping via Promtail, local OpenTelemetry export to the central Traceway, Docker engine telemetry collection (container state, stats, logs, health), HTTP probe execution, a registration call on first boot, periodic heartbeat reporting to the control-plane API, and an action executor that processes approved remote commands such as container restart and log fetch. The agent maintains a local SQLite buffer that absorbs telemetry during central-plane outages and replays it on reconnection.'));

  b.push(h3('3.3.4  Communication Patterns'));
  b.push(p('Three communication patterns are present in the system. (i) Pull-based metric scraping: the central Prometheus federates from satellite Prometheus instances using HTTP scraping. (ii) Push-based log and trace shipping: Promtail and the satellite OTLP exporter push to the central Loki and Traceway over HTTPS. (iii) Bidirectional REST-over-HTTPS: satellites register and heartbeat to the control plane over short-lived HTTP requests; the control plane queues remote actions which satellites poll for on their heartbeat. WebSocket upgrade is supported for low-latency log streaming when an operator opens a container log view.'));

  b.push(h3('3.3.5  High-Level Architecture'));
  b.push(p('Figure 3.1 presents the high-level architecture as a layered diagram. The central control plane decomposes into the FastAPI service, the reasoning agent, the remediation engine, the LLM provider abstraction, the RAG service, the policy engine, the audit service, the dashboard, the Traceway subsystem, the notification dispatcher, and the PostgreSQL store. External components include the six LLM providers, the two Git providers (GitHub, GitLab), the upstream scanner sources, and the satellite fleet — N remote servers each running a satellite container alongside the workload containers. All cross-boundary traffic is HTTPS.'));
  b.push(blank());
  b.push(image('figures/fig_3_1_architecture.png', { w: 7.5, h: 4.7 }));
  b.push(pCenter('Figure 3.1: InfraGuard Pro — High-Level System Architecture.'));
  b.push(blank());

  b.push(h3('3.3.6  Multi-Server Satellite Topology'));
  b.push(p('Figure 3.2 depicts the satellite topology as a star graph with the central control plane at the centre. Each spoke terminates in a representative LivWell satellite labelled with its environment tag (prod-af-1 in Lagos, prod-eu-1 in Frankfurt, prod-us-1 in Iowa, staging-eu-1 in Frankfurt, dev-local in the Lagos office). The dashed edges represent the 60-second HTTPS heartbeat carrying OTLP telemetry and the REST poll for queued remote actions. An inset summarises the internal composition of a typical satellite: the agent process and its SQLite buffer, a local Prometheus and Promtail, a CrowdSec instance, and the customer workload containers.'));
  b.push(blank());
  b.push(image('figures/fig_3_2_topology.png', { w: 7.5, h: 4.7 }));
  b.push(pCenter('Figure 3.2: Multi-Server Satellite Deployment Topology.'));
  b.push(blank());

  b.push(h3('3.3.7  Remediation Engine Data Flow'));
  b.push(p('Figure 3.3 traces the end-to-end data flow of a single finding through the Remediation Engine. The flow begins at the CI/CD pipeline, which uploads a SARIF document to the control plane. The SARIF document is parsed and normalised; for each finding, retrieval is performed against the RAG corpus; the retrieved context is composed into a structured prompt and dispatched to the active LLM provider; the returned patch is classified by the policy engine; if the policy permits autonomous action, the Git provider adapter opens a pull request, otherwise the patch enters the human-approval queue; merged patches trigger a re-run of the originating scanner against the patched artefact; the post-deploy observation window opens, during which the runtime telemetry is watched; finally the remediation is marked successful, failed, or rolled back, and the outcome is indexed back into the RAG corpus. Every step emits a hash-chained audit log entry.'));
  b.push(blank());
  b.push(image('figures/fig_3_3_remediation_flow.png', { w: 7.5, h: 4.4 }));
  b.push(pCenter('Figure 3.3: Autonomous Remediation Engine — End-to-End Data Flow.'));
  b.push(blank());

  // 3.4 SYSTEM DESIGN
  b.push(h2('3.4  System Design'));
  b.push(p('This section presents the detailed design of the system, including the database schema, the principal class hierarchy, the sequence of operations for the canonical remediation workflow, and the state machine that governs the reasoning agent.'));

  b.push(h3('3.4.1  Database Design (Entity-Relationship Model)'));
  b.push(p('The relational schema captures eight principal entities. Figure 3.6 presents the entity-relationship diagram; the textual schema below provides field-level detail for the most important tables.'));
  b.push(h4('Entity: satellites'));
  b.push(p('Columns: id (PK, UUID), label (TEXT), ip (INET), environment (ENUM: prod, staging, dev), region (TEXT), status (ENUM: online, offline, degraded), last_heartbeat (TIMESTAMPTZ), container_count (INTEGER), registered_at (TIMESTAMPTZ).'));
  b.push(h4('Entity: containers'));
  b.push(p('Columns: id (PK, UUID), satellite_id (FK → satellites), name (TEXT), image (TEXT), status (TEXT), health (TEXT), cpu_pct (REAL), memory_bytes (BIGINT), restart_count (INTEGER), ports (JSONB), last_error (TEXT), updated_at (TIMESTAMPTZ).'));
  b.push(h4('Entity: findings'));
  b.push(p('Columns: id (PK, UUID), source_scanner (TEXT), rule_id (TEXT), cwe (TEXT), cve (TEXT), cvss (REAL), severity (ENUM: low, medium, high, critical), file_path (TEXT), line_start (INTEGER), line_end (INTEGER), message (TEXT), sarif_raw (JSONB), ingested_at (TIMESTAMPTZ).'));
  b.push(h4('Entity: remediations'));
  b.push(p('Columns: id (PK, UUID), finding_id (FK → findings), llm_provider (TEXT), llm_model (TEXT), patch_diff (TEXT), confidence (REAL), evidence_refs (JSONB), policy_mode (ENUM: recommend, approval, autonomous), pr_url (TEXT), pr_status (ENUM: open, merged, rejected, closed), created_at (TIMESTAMPTZ).'));
  b.push(h4('Entity: validations'));
  b.push(p('Columns: id (PK, UUID), remediation_id (FK → remediations), rescan_status (ENUM: pass, fail, error), runtime_regression (BOOLEAN), observation_window_start (TIMESTAMPTZ), observation_window_end (TIMESTAMPTZ), outcome (ENUM: success, failure, rolled_back).'));
  b.push(h4('Entity: verdicts'));
  b.push(p('Columns: id (PK, AUTOINCREMENT), created_at (TIMESTAMPTZ), severity (TEXT), summary (TEXT), payload (JSONB), satellite_id (FK → satellites NULL).'));
  b.push(h4('Entity: audit_log'));
  b.push(p('Columns: id (PK, AUTOINCREMENT), timestamp (TIMESTAMPTZ), actor (TEXT), action (TEXT), entity_type (TEXT), entity_id (UUID), details (JSONB), prev_hash (CHAR(64)), hash (CHAR(64)).'));
  b.push(h4('Entity: users'));
  b.push(p('Columns: id (PK, UUID), username (TEXT, UNIQUE), password_hash (TEXT), role (ENUM: admin, operator, viewer), created_at (TIMESTAMPTZ), last_login (TIMESTAMPTZ).'));

  b.push(h3('3.4.2  Use-Case Model'));
  b.push(p('Figure 3.4 presents the use-case diagram. The DevSecOps Operator interacts with the system through the dashboard for verdict review, patch approval, provider switching, validation inspection, rollback, and runbook search. The Developer receives pull-request notifications. The CI/CD Pipeline acts as the producer of SARIF input. The LLM Provider is an external system invoked by the Remediation Engine.'));
  b.push(blank());
  b.push(image('figures/fig_3_4_usecase.png', { w: 7.0, h: 4.9 }));
  b.push(pCenter('Figure 3.4: Use-Case Diagram — DevSecOps Operator.'));
  b.push(blank());

  b.push(h3('3.4.3  Sequence Diagram: SARIF to Pull Request'));
  b.push(p('Figure 3.5 shows the canonical end-to-end workflow. The CI/CD pipeline POSTs a SARIF document; the SARIF adapter normalises and persists findings; the remediation engine queries the RAG service for top-k runbook chunks and historical fix records; the active LLM provider returns a structured patch proposal; the policy engine assigns a mode; the Git provider adapter opens a pull request (autonomous mode) or queues the proposal for operator approval; on merge, a webhook triggers the validator to re-run the originating scanner and observe runtime telemetry; the outcome is recorded and indexed back into the RAG corpus. Every step generates a hash-chained audit log entry.'));
  b.push(blank());
  b.push(image('figures/fig_3_5_sequence.png', { w: 7.5, h: 5.0 }));
  b.push(pCenter('Figure 3.5: Sequence Diagram — SARIF Ingestion to Merged Pull Request.'));
  b.push(blank());

  b.push(h3('3.4.4  Entity-Relationship Model'));
  b.push(p('Figure 3.6 visualises the relational schema described above. The principal cardinalities are: one satellite to many containers, one satellite to many verdicts, one finding to one remediation (lifecycle one-to-one), one remediation to one validation outcome, and one user to many audit entries.'));
  b.push(blank());
  b.push(image('figures/fig_3_6_erd.png', { w: 7.5, h: 4.7 }));
  b.push(pCenter('Figure 3.6: Entity-Relationship Diagram of the Verdict and Remediation Schema.'));
  b.push(blank());

  b.push(h3('3.4.5  Class Diagram: LLM Provider Abstraction'));
  b.push(p('The LLM provider abstraction follows the strategy pattern (Figure 4.2). The abstract LLMProvider declares the async reason(context) → Verdict and health_check() methods. Concrete subclasses VertexAIProvider, OpenAIProvider, AnthropicProvider, KimiProvider, OllamaProvider, and LMStudioProvider each implement the contract using their respective vendor SDK or HTTP client. A ProviderRegistry maintains the mapping from provider identifier to concrete instance and exposes get_active(), set_active(provider_id, model_id), and list_available(). A ProviderHealthMonitor periodically probes each registered provider and exposes liveness state to the registry, which uses it to short-circuit calls to dead providers and fall back to a configured secondary. The class diagram is reproduced in Chapter Four (Figure 4.2) for reference.'));

  b.push(h3('3.4.6  State Machine: LangGraph Reasoning Agent'));
  b.push(p('Figure 3.7 depicts the LangGraph state machine that governs the reasoning agent. Six principal states — Collect, Retrieve, Analyse, Classify, Remediate, Validate — are traversed in sequence on the success path. An explicit error transition routes to a Notify state on any unrecoverable failure. A Reflexion-style retry loop (capped at three iterations) routes Validate failures back to Analyse with the failed-patch context attached to the prompt.'));
  b.push(blank());
  b.push(image('figures/fig_3_7_state_machine.png', { w: 7.5, h: 3.7 }));
  b.push(pCenter('Figure 3.7: State Machine of the LangGraph Reasoning Agent.'));
  b.push(blank());

  b.push(h3('3.4.7  Workflow: Multi-Source RAG Indexing'));
  b.push(p('Runbook indexing proceeds as a separate, lower-frequency workflow. On a configurable schedule (default daily, plus on-demand via POST /api/runbooks/index), the indexer iterates over the four configured sources. For Notion, it queries the configured database via the Notion API, extracts page content recursively, and converts to Markdown. For local Markdown, it walks the configured /runbooks volume mount. For uploaded artefacts, it consumes the uploads queue. For historical verdicts, it pulls successful, failure, and rolled-back remediation records since the last indexing run. Each document is chunked, embedded via the Vertex AI text-embedding-004 model, and upserted into ChromaDB with metadata identifying its source, ingest date, and (for historical verdicts) outcome. On retrieval, queries return the top-k chunks irrespective of source, allowing the LLM to consult organisational runbooks and historical fixes in the same context.'));

  // 3.5 TOOLS AND TECHNOLOGIES
  b.push(h2('3.5  Tools and Technologies Used'));
  b.push(p('The complete tools-and-technologies bill of materials for the project is summarised below, grouped by layer.'));
  b.push(h3('3.5.1  Backend'));
  b.push(bullet('Language: Python 3.11+'));
  b.push(bullet('Web framework: FastAPI 0.110+'));
  b.push(bullet('ASGI server: Uvicorn with the gunicorn worker class for production'));
  b.push(bullet('LLM orchestration: LangGraph 0.2.x, LangChain 0.3.x'));
  b.push(bullet('LLM SDKs: google-cloud-aiplatform, openai, anthropic, ollama, httpx (for Kimi and LM Studio OpenAI-compatible endpoints)'));
  b.push(bullet('Vector store: ChromaDB 0.5.x'));
  b.push(bullet('Relational ORM and migrations: SQLAlchemy 2.x with Alembic'));
  b.push(bullet('Async DB drivers: asyncpg (PostgreSQL), aiosqlite (SQLite buffer on satellites)'));
  b.push(bullet('Auth and sessions: itsdangerous URLSafeTimedSerializer, bcrypt for password hashing'));
  b.push(bullet('Git provider clients: PyGithub (GitHub), python-gitlab (GitLab)'));
  b.push(bullet('SARIF parsing: sarif-om plus a custom thin adapter'));
  b.push(bullet('Testing: pytest, pytest-asyncio, respx, hypothesis'));
  b.push(h3('3.5.2  Frontend'));
  b.push(bullet('Framework: SvelteKit 5 with Svelte 5'));
  b.push(bullet('Styling: Tailwind CSS 4'));
  b.push(bullet('State management: Svelte 5 runes (built-in)'));
  b.push(bullet('Charting: D3-svelte plus uPlot for high-cardinality time series'));
  b.push(bullet('Build tooling: Vite 5'));
  b.push(h3('3.5.3  Observability'));
  b.push(bullet('Metrics: Prometheus (federated)'));
  b.push(bullet('Logs: Loki + Promtail'));
  b.push(bullet('Traces, exceptions, AI tracing: Traceway (self-hosted)'));
  b.push(bullet('Telemetry protocol: OpenTelemetry (OTLP/HTTP)'));
  b.push(h3('3.5.4  Security'));
  b.push(bullet('IP threat response: CrowdSec local API'));
  b.push(bullet('Image scanning: Trivy (also a target of the remediation engine)'));
  b.push(bullet('Secret detection: Gitleaks (also a target)'));
  b.push(bullet('SAST: Semgrep, Bandit (also targets)'));
  b.push(bullet('IaC scanning: Checkov (also a target)'));
  b.push(bullet('Dependency scanning: OSV-Scanner, Trivy filesystem mode (also targets)'));
  b.push(h3('3.5.5  Deployment'));
  b.push(bullet('Containerisation: Docker 25.x'));
  b.push(bullet('Orchestration (development and small deployments): Docker Compose v2'));
  b.push(bullet('Infrastructure-as-code (GCP): Terraform 1.6+'));
  b.push(bullet('CI/CD: GitHub Actions (primary), GitLab CI (secondary)'));
  b.push(bullet('Artefact registry: GitHub Container Registry, Google Artefact Registry'));
  b.push(h3('3.5.6  Supported LLM Providers'));
  b.push(p('Table 3.3 enumerates the LLM providers wired into the abstraction layer along with their key operational characteristics.'));
  b.push(blank());

  const llmColWidths = [1500, 1500, 1700, 1500, 1500, 1326];
  const llmHeaders = ['Provider', 'Reference Model', 'Hosting', 'Strengths', 'Weaknesses', 'Approx. USD per Million Output Tokens'];
  const llmRows = [
    llmHeaders,
    ['Google Vertex AI', 'gemini-2.5-flash', 'Managed cloud (GCP)', 'Low latency, generous free tier, native GCP integration, multimodal.', 'GCP service-account configuration overhead; per-region quotas.', '$0.30'],
    ['OpenAI', 'gpt-4o', 'Managed cloud', 'Highest-quality general reasoning; mature ecosystem.', 'Premium pricing; rate-limit complexity; data egress.', '$10.00'],
    ['Anthropic', 'claude-3-5-sonnet', 'Managed cloud', 'Best-in-class for code; strong refusal calibration.', 'Premium pricing; only one region at time of writing.', '$15.00'],
    ['Moonshot AI', 'kimi-k2', 'Managed cloud (CN)', 'OpenAI-compatible API; competitive pricing; strong Chinese-language support.', 'Geopolitical compliance considerations for non-Asian deployments.', '$2.00'],
    ['Ollama (self-hosted)', 'llama3.1:8b, deepseek-r1:7b', 'On-premises', 'Zero per-token cost; full data sovereignty; offline operation.', 'Requires local GPU for acceptable latency; lower quality than frontier models.', '$0.00'],
    ['LM Studio (self-hosted)', 'OpenAI-compatible local', 'On-premises', 'Mac-first GUI; multi-model swap.', 'Single-machine scale; lower throughput than Ollama in headless mode.', '$0.00'],
  ];
  b.push(buildTable(llmColWidths, llmRows));
  b.push(blank());
  b.push(p('Table 3.3: Supported LLM Providers and Their Capabilities. Token-cost figures are approximate and reflect public list pricing at the time of writing.', { align: require('docx').AlignmentType.CENTER }));

  return b;
}

module.exports = { chapter3 };
