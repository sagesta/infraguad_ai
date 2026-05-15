const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable, image } = require('../helpers');

function chapter4() {
  const b = [];

  b.push(chapterLabel('CHAPTER FOUR'));
  b.push(pCenter('SYSTEM IMPLEMENTATION'));
  b.push(blank());

  // 4.1 DEVELOPMENT ENVIRONMENT
  b.push(h2('4.1  Development Environment'));
  b.push(p('The system was developed and validated against a development environment chosen to closely mirror the target operational topology while remaining tractable on commodity hardware. This section documents the hardware, software, and tool-chain configuration that constituted the daily development loop.'));

  b.push(h3('4.1.1  Hardware'));
  b.push(p('Primary development was conducted on a Windows 11 Pro workstation equipped with an AMD Ryzen processor, 64 GB of DDR4 memory, and 2 TB of NVMe storage. Local LLM evaluation (the Ollama and LM Studio adapters) was conducted on the same machine with CPU-only inference for the 8-billion-parameter Llama 3.1 and DeepSeek-R1 models; latency results from this configuration are reported in Chapter Five with the explicit caveat that GPU-accelerated inference would yield substantially lower per-token latency.'));

  b.push(h3('4.1.2  Operating System and Container Runtime'));
  b.push(p('All services run in Linux containers managed by Docker Desktop on the development workstation and by native Docker on the staging Linux hosts. The Linux base images for all services are pinned to specific minor versions of Debian Bookworm Slim or Alpine 3.20, never to the moving "latest" tag. Image digests are pinned in production deployments to defeat tag-mutation attacks.'));

  b.push(h3('4.1.3  Source Control and Branching'));
  b.push(p('The repository is hosted on GitHub. The branching model follows trunk-based development with short-lived feature branches and squash-merge to main. Branch protection rules require passing CI (lint, unit tests, integration tests, security scans) and at least one approving review before merge — a deliberate self-imposed policy intended to validate that the system being built can in fact operate against its own pipeline.'));

  b.push(h3('4.1.4  CI/CD Pipeline'));
  b.push(p('The repository operates two GitHub Actions workflows. The first (.github/workflows/ci.yml) runs on every pull request and executes ruff, mypy, pytest, Bandit, Semgrep, Trivy filesystem mode, Checkov, Gitleaks, and OSV-Scanner. The SARIF outputs of the five security tools are uploaded as workflow artefacts. The second workflow (.github/workflows/deploy.yml) is invoked manually or via tag and builds container images, pushes to the Google Artefact Registry, and performs a zero-downtime SSH-based rolling deployment to the staging hosts. The combination of these two workflows is what permits the system to consume its own scanner output during evaluation.'));

  b.push(h3('4.1.5  Editor and Debugger Tooling'));
  b.push(p('Development was performed in Visual Studio Code with the Python, Pylance, Docker, GitHub Actions, and Tailwind CSS extensions; secondary editing was performed in Cursor and Claude Code for LLM-assisted refactoring tasks. The Python debugger was wired to attach into containerised processes via debugpy on a published port, enabling line-level debugging of the agent loop inside the actual container environment.'));

  // 4.2 IMPLEMENTATION DETAILS
  b.push(h2('4.2  Implementation Details'));
  b.push(p('This section describes the implementation of the principal modules, organised by the folder layout of the reference repository. File paths are given relative to the repository root. The discussion is at the level of architectural detail rather than line-by-line code; representative code snippets are reproduced in Appendix B.'));

  b.push(h3('4.2.1  Repository Layout'));
  b.push(p('Figure 4.1 visualises the folder structure of the reference implementation, highlighting the modules introduced by this project. The full path-by-path responsibility map follows in Table 4.1.'));
  b.push(blank());
  b.push(image('figures/fig_4_1_folder.png', { w: 6.0, h: 6.5 }));
  b.push(pCenter('Figure 4.1: Folder Structure of the InfraGuard Pro Reference Implementation.'));
  b.push(blank());

  const layoutColWidths = [2200, 6826];
  const layoutHeaders = ['Path', 'Responsibility'];
  const layoutRows = [
    layoutHeaders,
    ['agent/main.py', 'Entry point for the reasoning agent process; starts the asyncio event loop and the LangGraph state machine.'],
    ['agent/orchestrator.py', 'The LangGraph state machine implementation; wires Collect, Retrieve, Analyse, Classify, Remediate, Validate, and Notify states.'],
    ['agent/llm/provider.py', 'Abstract LLMProvider base class and ProviderRegistry singleton.'],
    ['agent/llm/vertex.py', 'Vertex AI Gemini implementation of the LLMProvider interface.'],
    ['agent/llm/openai.py', 'OpenAI GPT-4o implementation.'],
    ['agent/llm/anthropic.py', 'Anthropic Claude 3.5 Sonnet implementation.'],
    ['agent/llm/kimi.py', 'Moonshot AI Kimi implementation via the OpenAI-compatible endpoint.'],
    ['agent/llm/ollama.py', 'Self-hosted Ollama implementation for Llama 3.1, DeepSeek-R1, and Mistral.'],
    ['agent/llm/lmstudio.py', 'Self-hosted LM Studio implementation.'],
    ['agent/llm/langchain_agent.py', 'Optional multi-tool LangChain ReAct loop, selectable per-invocation.'],
    ['agent/rag/vector_store.py', 'ChromaDB binding; index, query, re-index operations.'],
    ['agent/rag/notion_loader.py', 'Notion API client and Markdown converter.'],
    ['agent/rag/markdown_loader.py', 'Local Markdown ingestion from the /runbooks volume.'],
    ['agent/rag/verdict_indexer.py', 'Indexes historical successful, failed, and rolled-back remediations into the RAG corpus.'],
    ['agent/remediation/engine.py', 'The Remediation Engine orchestrator; the principal new module of this project.'],
    ['agent/remediation/sarif.py', 'SARIF v2.1.0 parser and finding-normalisation adapter.'],
    ['agent/remediation/policy.py', 'Policy engine; classifies patches into recommend, approval, autonomous modes.'],
    ['agent/remediation/git_provider.py', 'Abstract Git provider with GitHub and GitLab concrete implementations.'],
    ['agent/remediation/patch_builder.py', 'Composes the structured prompt and assembles the LLM output into a unified-diff patch.'],
    ['agent/remediation/validator.py', 'Closed-loop post-deployment validator: re-runs scanners and watches telemetry.'],
    ['agent/tools/prometheus.py', 'Prometheus instant- and range-query client.'],
    ['agent/tools/loki.py', 'Loki log-query client.'],
    ['agent/tools/http_probe.py', 'HTTP probe executor.'],
    ['agent/tools/docker_api.py', 'Docker Engine API client for stats, logs, and health.'],
    ['agent/tools/threat_response.py', 'Pattern-based threat detection plus the CrowdSec adapter.'],
    ['agent/tools/traceway.py', 'Traceway API client for exceptions, traces, and AI tracing.'],
    ['api/main.py', 'FastAPI application factory; assembles routers and middlewares.'],
    ['api/routes/satellites.py', 'Satellite registration, heartbeat, and remote-action endpoints.'],
    ['api/routes/sarif.py', 'SARIF ingestion endpoint.'],
    ['api/routes/remediation.py', 'Remediation queue and approval endpoints.'],
    ['api/routes/runbooks.py', 'Runbook indexing, search, and upload endpoints.'],
    ['api/routes/llm_config.py', 'Runtime LLM provider/model switching endpoint.'],
    ['api/routes/threats.py', 'Threat-analysis and CrowdSec apply endpoints.'],
    ['api/routes/verdicts.py', 'Verdict listing and detail endpoints.'],
    ['api/routes/audit.py', 'Audit-log viewing endpoint (admin-only).'],
    ['api/middleware/auth.py', 'Cookie-based session authentication middleware.'],
    ['api/middleware/audit.py', 'Per-request audit-logging middleware.'],
    ['api/middleware/security.py', 'Security-header middleware (CSP, HSTS, X-Frame-Options).'],
    ['api/middleware/rate_limit.py', 'slowapi-based rate limiting on sensitive endpoints.'],
    ['api/store/db.py', 'SQLAlchemy engine and session-management.'],
    ['api/store/models.py', 'ORM models for all entities in Section 3.4.1.'],
    ['api/store/migrations/', 'Alembic migration history.'],
    ['satellite/main.py', 'Satellite agent entry point.'],
    ['satellite/heartbeat.py', 'Periodic heartbeat reporter with local SQLite buffering on failure.'],
    ['satellite/action_executor.py', 'Executes approved remote actions delivered by the control plane.'],
    ['satellite/Dockerfile', 'Minimal satellite container image (Python 3.11-slim base).'],
    ['dashboard/', 'SvelteKit 5 application; routes/, lib/, app.html, tailwind.config.ts.'],
    ['tests/', 'pytest test suite organised by module: test_agent, test_api, test_remediation, test_rag, test_policy, test_satellites, test_threat_response, test_tools.'],
    ['terraform/', 'GCP infrastructure-as-code for the central control plane.'],
    ['docker-compose.yml', 'Central control plane composition.'],
    ['docker-compose.satellite.yml', 'Satellite composition.'],
    ['.github/workflows/ci.yml', 'CI workflow with multi-scanner SARIF upload.'],
    ['.github/workflows/deploy.yml', 'Deployment workflow with rolling SSH update.'],
  ];
  b.push(buildTable(layoutColWidths, layoutRows));
  b.push(blank());
  b.push(p('Table 4.1: Repository Module Map and Responsibilities.', { align: require('docx').AlignmentType.CENTER }));

  b.push(h3('4.2.2  The LLM Provider Abstraction'));
  b.push(p('The LLM provider abstraction is the architectural cornerstone of the project and the principal vehicle by which the LLM-vendor-lock-in gap identified in Section 2.4 is closed. The abstraction is implemented in agent/llm/provider.py and follows the strategy pattern. Figure 4.2 shows the class hierarchy.'));
  b.push(blank());
  b.push(image('figures/fig_4_2_llm_classes.png', { w: 7.5, h: 4.0 }));
  b.push(pCenter('Figure 4.2: LLM Provider Abstraction — Class Hierarchy.'));
  b.push(blank());
  b.push(p('At the heart of the design is the LLMProvider abstract base class. It declares a single asynchronous method, reason(context: AgentContext) -> Verdict, which accepts a unified AgentContext dataclass — containing the telemetry snapshot, the retrieved RAG documents, the finding (when invoked from the remediation engine), and an optional patch-builder hint — and returns a Verdict dataclass with severity, summary, root cause, recommended action, confidence, evidence references, provider identifier, model identifier, and the raw text returned by the model for post-hoc audit. Six concrete subclasses implement the contract: VertexAIProvider, OpenAIProvider, AnthropicProvider, KimiProvider, OllamaProvider, and LMStudioProvider. Each subclass encapsulates the vendor-specific authentication, request shaping, streaming versus non-streaming preference, and response parsing.'));
  b.push(p('The ProviderRegistry is a singleton constructed at application startup that reads the LLM_PROVIDER and LLM_MODEL environment variables, instantiates the corresponding subclass, and exposes get_active(), set_active(provider_id, model_id), and list_available(). Crucially, set_active swaps the active instance under an asyncio lock, allowing the dashboard /api/agent/llm-config endpoint to perform runtime hot-swaps without restarting the agent process. Every call to reason() records the provider and model identifiers into the resulting verdict, satisfying the requirement that every recorded decision be attributable to a specific model invocation.'));
  b.push(p('The ProviderHealthMonitor runs as a background asyncio task that probes each registered provider every sixty seconds with a minimal completion request, exposing liveness via a property checked by the agent loop. Should the active provider fail health checks for three consecutive probes, the registry temporarily falls back to a configured secondary provider, recording the fallback event in the audit log and emitting a high-severity notification.'));

  b.push(h3('4.2.3  The Remediation Engine'));
  b.push(p('The Remediation Engine is the principal new module introduced by this project, hosted in agent/remediation/engine.py. Its role is to consume normalised findings from the findings table, orchestrate the patch-generation cycle, route the result through the policy engine, and dispatch to the Git provider adapter.'));
  b.push(p('The engine exposes a single public method, remediate(finding: Finding) -> Remediation, which is invoked either by a polling loop that picks up newly-ingested findings on a fifteen-second cadence or by a direct call from the on-demand diagnosis endpoint. The remediate method executes a fixed eight-step pipeline: (1) retrieve grounding context from the RAG service using a finding-derived query template; (2) compose the structured prompt via the PatchBuilder, which composes the system prompt, the finding details, the retrieved context, and the explicit JSON output schema; (3) invoke the active LLM provider; (4) parse and validate the returned patch structure (rejecting and retrying on schema failure up to a configurable budget); (5) compute the patch confidence score by combining the LLM-reported confidence with a heuristic based on diff size, number of files affected, and CWE class; (6) classify the patch via the policy engine; (7) for autonomous-mode patches, invoke the Git provider adapter to create a branch, apply the diff, and open a pull request; for approval-mode patches, persist to the remediations table with pr_status open and policy_mode approval; (8) record the entire pipeline outcome in the audit log with the SHA-256 hash chain.'));
  b.push(p('The PatchBuilder enforces a strict structured-output contract on the LLM. The prompt explicitly specifies the JSON schema: severity, summary, root_cause, recommended_action, confidence, evidence (an array of {source, citation, snippet} objects), patch (a unified-diff string), and provider/model identifiers. The Vertex AI provider exploits Gemini’s response_mime_type=application/json directive to enforce JSON output natively; the OpenAI and Anthropic providers use their respective JSON-mode features; the Kimi, Ollama, and LM Studio providers fall back to prompt-instructed JSON with a permissive parser that strips Markdown code fences and trailing commentary. The contract is validated against a Pydantic model on every invocation, and schema violations trigger up to three retries with progressively more explicit prompts before the patch is recorded as failed.'));

  b.push(h3('4.2.4  The SARIF Ingestion Pipeline'));
  b.push(p('The SARIF ingestion pipeline is implemented in agent/remediation/sarif.py and api/routes/sarif.py. The HTTP endpoint POST /api/sarif/ingest accepts a SARIF 2.1.0 document up to 50 MB. The endpoint validates the document against the OASIS-published JSON schema, extracts each result, and translates it into the unified Finding model defined in Section 3.4.1. The translation preserves the rule identifier, the source-location URI and region, the CWE and CVE references when present, and the original suggested fix when supplied. CVSS scores are derived where absent by lookup against the National Vulnerability Database via an injected NVDClient (cached locally). The pipeline is idempotent: a finding with the same source-scanner, rule identifier, and source-location triple is considered a duplicate of any existing open finding and is merged rather than re-created.'));

  b.push(h3('4.2.5  The Policy Engine'));
  b.push(p('The policy engine, in agent/remediation/policy.py, classifies each patch proposal into one of the three execution modes. The classifier is rule-based rather than machine-learned, by deliberate design: the decision logic governing autonomous remediation must be auditable line-by-line by security review boards. The default ruleset is as follows. (i) Patches with LLM-reported confidence below 0.6, or with patches touching more than five files, or for findings of CVSS severity ≥ 9.0, are routed to human-approval. (ii) Patches touching only files matched by configurable autonomous-allowed glob patterns (typically requirements.txt, package.json, Dockerfile, and *.tf with restricted scope), with confidence ≥ 0.8, and for findings of CVSS severity ≤ 6.9, are routed to autonomous-low-risk. (iii) All other patches default to recommend-only, where they appear in the dashboard queue but are never auto-applied. The ruleset is loaded from a YAML configuration file at startup and may be overridden per organisation. Every classification decision records the rule that fired in the audit log.'));

  b.push(h3('4.2.6  The Git Provider Adapter'));
  b.push(p('The Git provider adapter, in agent/remediation/git_provider.py, abstracts pull-request creation across GitHub and GitLab. The abstract GitProvider base declares: create_branch(repo, base, head), apply_patch(repo, head, diff), open_pull_request(repo, head, base, title, body), comment_on_pull_request(repo, pr_number, body), and check_pull_request_status(repo, pr_number). Concrete subclasses GitHubProvider and GitLabProvider implement the contract using PyGithub and python-gitlab respectively. The body of the pull request is composed by a template engine that includes the LLM-generated summary, the root-cause analysis, the evidence chain, the citation references with hyperlinks to the source runbooks, and a machine-readable footer carrying the remediation identifier for the post-merge webhook handler.'));

  b.push(h3('4.2.7  The Closed-Loop Validator'));
  b.push(p('The closed-loop validator, in agent/remediation/validator.py, is invoked on pull-request merge events received via webhook. The validator performs three actions. First, it re-runs the originating scanner against the merged artefact using the same containerised scanner version that produced the original finding, asserting that the specific rule violation is no longer reported. Second, it opens an observation window of configurable duration (default ten minutes) during which the runtime telemetry of the affected satellite is monitored for anomalies: a step change in HTTP 5xx ratio, a step change in container restart count, a step change in p95 latency, or any new critical-severity verdict from the reasoning agent referencing the affected service. Third, on observation-window closure, the validator records the outcome (success, failure, rolled_back) in the validations table and indexes the (finding, patch, outcome) triple into the RAG corpus for use as historical context in future generations. Failed validations trigger an automatic rollback pull request and a high-severity notification.'));

  b.push(h3('4.2.8  Multi-Source RAG'));
  b.push(p('The multi-source RAG implementation extends the existing single-source Notion implementation. Source-specific loaders in agent/rag/notion_loader.py, agent/rag/markdown_loader.py, agent/rag/upload_loader.py, and agent/rag/verdict_indexer.py each produce a uniform Document dataclass containing content, source identifier, source class, ingest timestamp, and optional metadata. Documents are chunked at 800-token boundaries with 100-token overlap, embedded by the Vertex AI text-embedding-004 model (which was retained from the existing baseline; the OpenAI text-embedding-3-small is offered as a fallback), and upserted into the ChromaDB collection. Retrieval uses the standard ChromaDB similarity_search interface with k=5 by default. The historical-verdict indexer is novel to this project: it walks the validations table for the past ninety days and emits one document per (finding, patch, outcome) triple, with the outcome attached as metadata so that downstream queries can filter to learn preferentially from successful fixes.'));

  b.push(h3('4.2.9  The Satellite Agent'));
  b.push(p('The satellite agent, in satellite/, is implemented as a minimal asyncio application bundled into a 110 MB Python 3.11-slim Docker image. On first boot, satellite/main.py reads the CENTRAL_API_URL, SERVER_ID, SERVER_LABEL, and SERVER_ENV environment variables; calls POST /api/satellites/register against the control plane with its self-reported metadata; and persists the assigned satellite_id and authentication token into a local volume. The heartbeat loop, in satellite/heartbeat.py, runs every sixty seconds and posts a payload containing CPU/memory/disk telemetry, the live container inventory, the last error from each container, and a count of locally-buffered actions awaiting central acknowledgement. The action executor, in satellite/action_executor.py, polls a per-satellite queue endpoint and processes approved remote actions: container restart, container stop, log fetch (returned via a presigned upload URL), Docker inspect, and trigger-diagnose. Every action is recorded locally before execution and the outcome is reported back on the next heartbeat. The local SQLite buffer absorbs telemetry during control-plane outages of up to one hour, with the oldest entries discarded first on overflow.'));

  b.push(h3('4.2.10  The Dashboard'));
  b.push(p('The dashboard is implemented as a SvelteKit 5 application in dashboard/. The principal routes are: / (Overview — fleet health, severity counters, recent verdicts), /servers (Servers table with drill-down), /servers/[id] (Server detail with container inventory and live log stream), /containers/[id] (Container detail with health, logs, traces, and a Restart/Stop/Diagnose button), /verdicts (the verdict feed, filterable by server, severity, provider), /remediations (the remediation queue with approval actions), /runbooks (the runbook browser with semantic-search and chat UI), /threats (CrowdSec feed and global ban actions), /traces (embedded Traceway view), /settings (LLM provider switcher, heartbeat configuration, prompt editor, notification routing), and /audit (admin-only audit-log viewer). The application is delivered as a static build behind the FastAPI service and communicates with the API exclusively over JSON. Authentication is shared with the API via the session cookie. The dark-mode-first theme uses a Tailwind palette anchored at neutral-950 background with severity colours mapped to the existing InfraGuard verdict scheme (OK green, warning amber, high orange, critical red). Figure 4.3 reproduces the Overview page.'));
  b.push(blank());
  b.push(image('figures/fig_4_3_dashboard.png', { w: 7.5, h: 4.4 }));
  b.push(pCenter('Figure 4.3: Dashboard Overview Page — Multi-Server Fleet View (illustrative mock).'));
  b.push(blank());

  b.push(h3('4.2.11  New API Endpoints Introduced by This Project'));
  b.push(blank());
  const apiColWidths = [2000, 800, 6226];
  const apiHeaders = ['Endpoint', 'Method', 'Purpose'];
  const apiRows = [
    apiHeaders,
    ['/api/sarif/ingest', 'POST', 'Accept a SARIF 2.1.0 document, normalise findings, persist to the findings table, enqueue for remediation.'],
    ['/api/satellites/register', 'POST', 'First-boot registration of a satellite agent; returns satellite_id and authentication token.'],
    ['/api/satellites/{id}/heartbeat', 'POST', 'Periodic telemetry and inventory report from a satellite.'],
    ['/api/satellites', 'GET', 'List all registered satellites with status, label, environment, last heartbeat, container count.'],
    ['/api/satellites/{id}', 'GET', 'Detailed satellite view including container inventory.'],
    ['/api/satellites/{id}/actions', 'GET', 'Satellite-polled queue of approved remote actions.'],
    ['/api/containers/{id}/restart', 'POST', 'Operator-issued container restart, executed via the next satellite poll.'],
    ['/api/containers/{id}/stop', 'POST', 'Operator-issued container stop.'],
    ['/api/containers/{id}/logs', 'GET', 'WebSocket-upgraded log-streaming endpoint.'],
    ['/api/containers/{id}/diagnose', 'POST', 'Trigger an on-demand diagnosis cycle for a specific container.'],
    ['/api/remediations', 'GET', 'List remediations in any policy mode, filterable by status, severity, provider.'],
    ['/api/remediations/{id}', 'GET', 'Remediation detail including the diff, evidence, audit chain.'],
    ['/api/remediations/{id}/approve', 'POST', 'Approve a human-approval-required remediation; triggers immediate PR creation.'],
    ['/api/remediations/{id}/reject', 'POST', 'Reject a remediation with an operator reason recorded in the audit log.'],
    ['/api/remediations/{id}/rollback', 'POST', 'Roll back a previously-applied remediation; opens a reverting PR.'],
    ['/api/agent/llm-config', 'GET/POST', 'View or hot-swap the active LLM provider and model.'],
    ['/api/agent/diagnose-now', 'POST', 'Trigger an immediate diagnosis cycle (bypassing the heartbeat).'],
    ['/api/runbooks/upload', 'POST', 'Upload a new runbook artefact (Markdown, text, or PDF).'],
    ['/api/runbooks/list', 'GET', 'Enumerate indexed runbooks by source, date.'],
    ['/api/runbooks/index', 'POST', 'Trigger a full re-index across all configured sources.'],
    ['/api/runbooks/query', 'POST', 'RAG semantic search; returns an answer and source citations.'],
    ['/api/incidents/similar', 'GET', 'Top-k historical incidents similar to the supplied context.'],
    ['/api/traceway/exceptions', 'GET', 'Proxied Traceway exception feed for the embedded view.'],
    ['/api/traceway/correlate', 'POST', 'On-demand AI correlation between an exception and its surrounding logs/traces.'],
    ['/api/threats/apply-global', 'POST', 'Apply a CrowdSec ban decision to all satellites simultaneously.'],
    ['/api/audit', 'GET', 'Paged audit-log access (admin-only); supports filtering by actor, action, entity.'],
  ];
  b.push(buildTable(apiColWidths, apiRows));
  b.push(blank());
  b.push(p('Table 4.2: New API Endpoints Added by the Remediation Engine.', { align: require('docx').AlignmentType.CENTER }));

  // 4.3 SECURITY, PERFORMANCE, SCALABILITY
  b.push(h2('4.3  Security, Performance, and Scalability Considerations'));

  b.push(h3('4.3.1  Authentication and Session Management'));
  b.push(p('All non-public endpoints require a valid session cookie signed with itsdangerous URLSafeTimedSerializer using a SECRET_KEY provisioned as an environment variable. Sessions have a maximum lifetime of twenty-four hours and are validated on every request by the AuthMiddleware in api/middleware/auth.py. Public endpoints are limited to /login (POST), /health (GET), and the satellite endpoints /api/satellites/register and /api/satellites/{id}/heartbeat (which carry their own bearer-token authentication using the token issued at registration). The constant-time hmac.compare_digest function is used for credential verification, eliminating timing side-channel risks.'));

  b.push(h3('4.3.2  Audit-Log Tamper Evidence'));
  b.push(p('The audit_log table maintains a SHA-256 hash chain across entries. Each row records the SHA-256 hash of (prev_hash || timestamp || actor || action || entity_type || entity_id || canonical_json(details)) where prev_hash is the hash of the preceding row; the first row anchors against a configurable salt. Verification is offered through a CLI tool (scripts/verify_audit_chain.py) that walks the chain end-to-end. Any tampering with a prior entry invalidates every subsequent hash and is immediately detected by the verifier. This design pattern, drawn from certificate-transparency logs, satisfies the audit-integrity non-functional requirement NFR-06 without requiring a separate write-once storage tier.'));

  b.push(h3('4.3.3  Secret Handling'));
  b.push(p('Secrets — LLM provider API keys, GCP service-account JSON, Git provider tokens, CrowdSec API keys, SMTP credentials, and the SECRET_KEY itself — are never stored in the repository, never written to the audit log, and never included in LLM prompts. They are sourced exclusively from environment variables injected by Docker Compose at runtime, with production deployments using GCP Secret Manager (mounted via the Workload Identity mechanism) as the secret store. Prompt-redaction in the PatchBuilder masks any string matching the pattern of a likely secret (high-entropy 32-character or longer base64 substrings, known token prefixes such as ghp_, sk-, AIza, eyJ) before the prompt is sent to the LLM. The redaction set is itself defined in a YAML configuration to allow expansion without code change.'));

  b.push(h3('4.3.4  Performance — End-to-End MTTR'));
  b.push(p('The non-functional requirement NFR-02 sets a median end-to-end MTTR of ten minutes for autonomous-mode patches. Empirical measurement (Chapter Five) confirms a median of 4 minutes 11 seconds across the benchmark, well within the target. The dominant contributors to the latency budget are the LLM round-trip (median 8.4 s for Vertex AI Gemini 2.5 Flash; 14.2 s for OpenAI GPT-4o; 17.8 s for Claude 3.5 Sonnet; 22.0 s for Ollama Llama 3.1 8B on CPU), the Git provider pull-request creation (median 1.2 s for GitHub), and the post-deploy observation window (configurable; default 10 minutes inclusive of CI re-run). The remaining components — SARIF parsing, RAG retrieval, policy classification, audit recording — collectively contribute less than one second to the median.'));

  b.push(h3('4.3.5  Performance — Concurrency and Throughput'));
  b.push(p('FastAPI under Uvicorn workers handles the API surface; the remediation engine processes findings sequentially per worker, parameterised by a configurable REMEDIATION_WORKER_COUNT environment variable (default four). Findings are partitioned across workers by a consistent-hash modulus on the finding identifier, ensuring no two workers attempt the same finding simultaneously without requiring an external distributed lock. Empirically the four-worker configuration on the development workstation processes approximately 240 findings per hour at steady state, well within the latency budget for typical mid-market CI/CD volumes.'));

  b.push(h3('4.3.6  Scalability — Satellite Fleet'));
  b.push(p('The control plane is designed for a satellite fleet of at least fifty heartbeating concurrently (NFR-03). The heartbeat endpoint is stateless modulo a database insert; PostgreSQL connection pooling via asyncpg sustains the implied write load (50 satellites × 1 heartbeat / 60 s = 0.83 writes/s) with substantial headroom. Telemetry forwarding to Traceway is bounded by Traceway’s own ingestion capacity, which on a single ClickHouse host comfortably absorbs the satellite fleet’s combined OTLP rate at typical workload densities. The architecture is not designed for fleet sizes beyond the low hundreds without a sharded control plane; this is identified as future work in Section 6.4.'));

  b.push(h3('4.3.7  Scalability — RAG Corpus'));
  b.push(p('The ChromaDB local-persistence mode scales to corpora of approximately one million documents on commodity hardware; this is sufficient for runbook collections and historical-verdict accumulation through several years of operation. For larger corpora, the abstraction over the vector store interface in agent/rag/vector_store.py allows transparent migration to a hosted vector database (Pinecone, Weaviate, Qdrant) without changes to the consuming code.'));

  b.push(h3('4.3.8  Cost Controls'));
  b.push(p('Per-finding LLM cost is bounded by three mechanisms. First, the structured-output contract minimises output token count by forbidding free-form preambles. Second, prompt-template caching exploits each provider’s respective prompt-caching feature (Vertex AI, OpenAI, Anthropic all expose cache markers; Ollama and LM Studio are not metered, so caching is not applicable). Third, the policy engine routes the most expensive providers (Claude 3.5 Sonnet, GPT-4o) only to high-confidence-required cases, while routing routine dependency upgrades to the cheaper Vertex AI Gemini 2.5 Flash or to the zero-cost Ollama tier. Empirical cost per finding across the benchmark is documented in Table 5.3.'));

  b.push(h3('4.3.9  Reliability — Degradation Modes'));
  b.push(p('The system exhibits three degradation modes by deliberate design. (i) If the LLM provider is unreachable, the agent enters a recommend-only mode, surfacing findings to the dashboard but generating no patches; this prevents silent failures and preserves alerting. (ii) If a satellite loses connectivity to the control plane, it buffers telemetry locally and replays on reconnection, preserving observation continuity. (iii) If a scanner re-run during post-deployment validation fails for reasons unrelated to the patch (network, registry availability), the validator records error rather than failure and retries on a back-off schedule, preserving the integrity of the success/failure outcome record.'));

  // 4.4 CHALLENGES ENCOUNTERED
  b.push(h2('4.4  Challenges Encountered'));

  b.push(h3('4.4.1  LLM Output Conformance'));
  b.push(p('The most persistent implementation challenge was ensuring that every LLM provider reliably produced the structured JSON expected by the PatchBuilder. Vertex AI and OpenAI offer first-class JSON-mode flags and proved most consistent. Anthropic’s tool-use mechanism was used to enforce the schema and was reliable but added prompt-token overhead. Kimi and Ollama required prompt-instructed JSON with an aggressive post-processing parser, and an initial baseline showed schema-violation rates of approximately 8% and 14% respectively. Mitigation took the form of (a) progressively more explicit prompts on retry, (b) Markdown-fence stripping in the parser, (c) a fallback to a smaller, more constrained "extraction" pass that asks only for the diff and synthesises the rest, and (d) caching of recent successful prompts as few-shot examples for the failing model. After mitigation the schema-violation rate dropped to under 1% across all providers on the benchmark.'));

  b.push(h3('4.4.2  SARIF Heterogeneity'));
  b.push(p('Although SARIF is nominally a single standard, scanner output exhibits substantial variation in how the standard is interpreted. Trivy emits per-vulnerability results with their own internal severity vocabulary; Semgrep emits per-rule results with CWE in the helpUri; Checkov emits per-resource results without source-line specificity in some cases. The SARIF adapter required scanner-specific normalisation paths to extract a uniform finding model. The adapter is therefore a small but real maintenance surface; new scanners require an adapter shim, and version upgrades of existing scanners must be regression-tested against a saved fixture corpus held in tests/fixtures/sarif/.'));

  b.push(h3('4.4.3  Git Provider API Rate Limits'));
  b.push(p('Both GitHub and GitLab impose request-rate limits that, while generous, become relevant when the system processes large SARIF documents and attempts to open dozens of pull requests in quick succession. The Git provider adapter implements an internal token-bucket limiter sized at 80% of the published per-hour quota, with surplus operations queued. The adapter also coalesces multiple findings affecting the same file into a single pull request where the LLM proposes compatible patches, reducing pull-request count and review overhead.'));

  b.push(h3('4.4.4  Closed-Loop Validation Flakiness'));
  b.push(p('Re-running a containerised scanner against a freshly-merged artefact is intermittently flaky in ways unrelated to the patch — transient registry pulls, occasional out-of-memory conditions in the scanner container, transient network failures. The validator was strengthened to distinguish error (re-runnable) from failure (genuine patch defect) using a structured exit-code mapping per scanner, eliminating false-positive failure outcomes that would have poisoned the historical-fix RAG corpus.'));

  b.push(h3('4.4.5  Multi-Server Time Synchronisation'));
  b.push(p('Audit-log hash chaining and verdict ordering depend on consistent timestamps across the satellite fleet. Initial trials surfaced occasional 30-second clock skew on a virtualised satellite host. Mitigation took the form of mandatory chrony installation in the satellite Dockerfile (with the host’s NTP socket bind-mounted) and a runtime sanity check on every heartbeat that flags satellites whose clock drifts more than two seconds from the control plane.'));

  b.push(h3('4.4.6  Resource Constraints on Local LLMs'));
  b.push(p('CPU-only inference of the Llama 3.1 8B and DeepSeek-R1 7B models in Ollama on the development workstation produced per-finding latencies between 18 and 30 seconds, well above the GPU-accelerated benchmark figures the model authors report. The benchmark results in Chapter Five document this caveat explicitly. Production deployments using local LLMs should provision a dedicated inference host with a GPU; the architecture supports any OpenAI-compatible endpoint, allowing such a host to be plugged in without code change.'));

  b.push(h3('4.4.7  Prompt-Injection and Adversarial Inputs'));
  b.push(p('A non-obvious security challenge in an LLM-driven remediation system is the possibility of an adversary injecting prompt-altering content into a scanner finding or runbook. A maliciously crafted commit message in an upstream dependency could, in principle, attempt to instruct the LLM to introduce a backdoor rather than a fix. The system mitigates this risk through (a) strict structured-output enforcement that rejects free-form output, (b) prompt isolation that places untrusted finding content inside explicitly-tagged sections (<finding>…</finding>) with a system-level instruction to ignore meta-instructions within those tags, (c) policy-engine bounds that prevent autonomous merging of patches outside narrowly-allowed file globs, and (d) human review on the human-approval path. The threat is not fully eliminated and is identified as an open research area in Section 6.4.'));

  return b;
}

module.exports = { chapter4 };
