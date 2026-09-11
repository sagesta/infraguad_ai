# Product Requirements Document: InfraGuard AI

| Field | Value |
|---|---|
| Product | InfraGuard AI |
| Document version | 1.0 |
| Status | Implementation-backed draft |
| Last updated | 29 August 2026 |
| Product type | Self-hosted infrastructure observability and incident-triage agent |
| Primary deployment | One team, one host or small application environment |
| Current maturity | Functional prototype; suitable for a controlled pilot after the P0 readiness work in Section 15 |

## 1. Executive Summary

InfraGuard AI is a self-hosted operational assistant for small engineering teams that already have, or can provide, infrastructure telemetry but do not have enough time or specialist staff to interpret it continuously.

Every 120 seconds by default, an independent agent collects recent logs from Loki, metrics from Prometheus, HTTP endpoint results, and optional Docker events and error logs. A configured model evaluates a bounded telemetry snapshot and returns a structured verdict containing severity, a summary, a likely root cause, a recommended action, and a canonical condition signature. The verdict is stored in SQLite and presented through an authenticated dashboard. High and critical conditions can trigger an ntfy notification. The frozen benchmark found repeat-stable signatures in only 10 of 24 scenarios, so canonical form must not be described as dependable semantic stability.

The product also provides:

- deterministic detection of selected brute-force and port-scan patterns in Loki logs;
- operator-approved IP banning through CrowdSec, with a safe dry-run mode;
- a runbook assistant that conditions an advisory answer on retrieved local Markdown documents indexed in ChromaDB and returns source titles;
- integration-status and stale-agent visibility;
- stateful verdict memory, allowing an operator to acknowledge a recurring low-risk condition without permanently hiding changed or severe conditions.

InfraGuard AI is not an autonomous remediation platform. It diagnoses, explains, recommends, remembers operator decisions, and assists with a narrow operator-approved security action. It does not restart services, modify infrastructure, patch application code, or open pull requests.

## 2. Product Vision

Enable a small operations team to move from raw monitoring signals to an understandable, actionable incident assessment in one interface, without outsourcing all telemetry or operational control to a full observability SaaS platform.

### 2.1 Product promise

> When a monitored service changes state, InfraGuard AI should tell the operator what changed, why it probably matters, what evidence informed the conclusion, and what to do next, while keeping consequential actions under human control.

### 2.2 Product principles

1. **Bounded evidence:** Telemetry, runbook text, and operator questions are labelled as untrusted data and bounded separately from model instructions; answer support must still be checked rather than assumed.
2. **Human control:** Enforcement actions require explicit operator approval.
3. **Severe alerts always surface:** High and critical verdicts cannot be suppressed.
4. **Memory must self-invalidate:** Acknowledgements are tied to condition, prompt version, and model rather than being permanent global exclusions.
5. **Optional integrations are not incidents:** An unconfigured data source is shown as unavailable, not reported as an infrastructure failure.
6. **Useful before sophisticated:** The product targets a focused single-site workflow before multi-tenancy, fleet management, or autonomous remediation.

## 3. Problem Statement

Prometheus, Loki, Docker, and uptime probes can expose failures quickly, but they present their evidence through different tools and data formats. A small team must still correlate an error-rate increase with log messages, endpoint state, recent container events, and its internal recovery procedure. This creates four practical problems:

- **Slow triage:** An operator manually switches between tools before forming a diagnosis.
- **Specialist dependency:** Raw metrics and logs may be difficult for a developer or junior operator to interpret correctly.
- **Alert fatigue:** A known low-risk condition is repeatedly raised and reconsidered.
- **Unsafe automation pressure:** Teams may either avoid useful automation or automate destructive actions without adequate control.

InfraGuard AI addresses these problems by aggregating a bounded telemetry snapshot, producing a structured assessment, retaining operator memory, and supporting controlled actions.

## 4. Target Users and Stakeholders

### 4.1 Primary users

| User | Need | Product value |
|---|---|---|
| Solo DevOps engineer | Monitor several services without watching multiple dashboards continuously | Unified verdict, notification, history, and runbook guidance |
| Small SaaS engineering team | Understand failures without a dedicated 24/7 SRE team | Faster first assessment and a shared operational view |
| On-call developer | Translate unfamiliar logs and metrics into next steps | Plain-language root cause and recommended action |
| IT administrator for an internal system | Detect outages and repeated hostile traffic | Endpoint monitoring, threat panel, and operator-approved blocking |
| Student or training laboratory | Demonstrate practical AIOps, observability, RAG, and safe automation | Deployable end-to-end reference system |

### 4.2 Secondary stakeholders

- Service owners whose applications are monitored.
- Security administrators responsible for CrowdSec or firewall policy.
- Runbook owners maintaining local Markdown procedures.
- Platform administrators responsible for deployment, networking, model API keys, and secrets.
- Auditors reviewing operator actions and application access logs.

## 5. Real-World Applicability

### 5.1 Strong-fit scenarios

#### Scenario A: Small SaaS API outage

An API begins returning HTTP 500 responses after a deployment. Loki contains database timeout messages, Prometheus shows an increased 5xx ratio, and the HTTP probe fails. InfraGuard AI correlates the supplied signals, produces a high or critical verdict, recommends checking database connectivity or rolling back, stores the evidence, and sends a push notification.

**Intended value:** Help the operator reach a first diagnosis. Any reduction in diagnosis time remains unmeasured, and the operator still validates and performs the rollback.

#### Scenario B: Resource pressure on a self-hosted application

Prometheus reports declining available memory or disk capacity. The agent produces a warning with the affected resource. The operator confirms that a temporary workload explains the condition and marks it as known. Matching low-risk repeats are suppressed until the acknowledgement expires or the condition/ruleset changes. A high or critical escalation still appears.

**Practical value:** Reduces repeated noise without creating a permanent blind spot.

#### Scenario C: Endpoint availability monitoring

One of the configured public or internal endpoints times out or returns a failing status. The dashboard displays the verdict, latency, likely scope, and response guidance; the stale-agent banner separately indicates whether InfraGuard itself has stopped reporting.

**Practical value:** Separates a monitored-service failure from a monitoring-agent failure.

#### Scenario D: Repeated hostile authentication traffic

Loki receives enough authentication failures from one source IP to cross a deterministic threshold. The threat panel presents the pattern and evidence count. The operator reviews it and selects **Block IP**. InfraGuard creates the CrowdSec decision server-side and applies it only when CrowdSec is configured; otherwise it records a dry-run result.

**Intended value:** Support a routine defensive workflow while preserving human approval. A time-saving effect has not been measured.

#### Scenario E: Incident procedure lookup

An on-call developer asks how to recover the database or restart a failed service. The runbook assistant retrieves relevant local runbook content from ChromaDB and asks the configured model to answer only from that material, returning source titles.

**Practical value:** Makes internal procedures easier to find during an incident.

### 5.2 Limited-fit scenarios

| Environment | Current suitability | Reason |
|---|---|---|
| One small team and one application environment | Good pilot fit | Matches the current single-site architecture and static administrator model |
| Development, staging, laboratory, or internal service | Good fit | Lower availability and compliance risk; dry-run security response is useful |
| Small production workload | Conditional fit | Requires all P0 production-readiness gates in Section 15 |
| Multi-tenant SaaS or managed-service provider | Not currently suitable | No tenant isolation, RBAC, agent registration, or fleet management |
| Highly regulated or sensitive environment | Not currently suitable | Telemetry redaction, encryption-at-rest policy, audit hardening, and formal data governance are incomplete |
| Safety-critical or automatic-remediation environment | Not suitable | LLM verdicts are advisory and the product has no validated autonomous remediation controller |

## 6. Goals and Non-Goals

### 6.1 Product goals

- G-01: Consolidate configured operational signals into one recurring analysis cycle.
- G-02: Produce a concise, structured, evidence-bounded infrastructure verdict.
- G-03: Help an operator reach a first actionable hypothesis faster than manual tool switching.
- G-04: Notify the operator when severity reaches high or critical.
- G-05: Reduce repeated low-risk verdict noise with self-invalidating memory.
- G-06: Detect selected threat patterns deterministically and keep blocking human-approved.
- G-07: Provide advisory access to organisation-specific runbooks with retrieved source titles and a human-review boundary.
- G-08: Remain straightforward to deploy and operate on a single host with Docker Compose.
- G-09: Expose failures in InfraGuard itself through staleness and integration state.

### 6.2 Non-goals for the current release

- Automatic restart, rollback, scaling, patch generation, or pull-request creation.
- Replacement for Prometheus, Loki, Grafana, CrowdSec, a SIEM, or an incident-management platform.
- General-purpose security detection beyond the implemented log patterns.
- Multi-tenant isolation, per-user permissions, SSO, or enterprise RBAC.
- High-availability control-plane operation or multi-region fleet management.
- Distributed tracing ingestion.
- Guaranteed root-cause correctness; all verdicts remain operator-reviewed hypotheses.

## 7. Current Product Baseline

The following capabilities exist in the repository as of 29 August 2026.

| Capability | Current implementation |
|---|---|
| Scheduled monitoring | Async heartbeat loop; default interval 120 seconds |
| Logs | Loki `query_range`, explicit 15-minute window, configurable result limit |
| Metrics | Prometheus CPU, available-memory, root-disk, and HTTP 5xx queries |
| Availability | HTTP status and latency probes for configured URLs |
| Containers | Optional Docker event, log, health, and diagnostic collection |
| AI reasoning | Gemini 2.5 Flash through direct and LangChain modes |
| Verdict | `ok`, `warning`, `high`, or `critical`, plus summary, root cause, action, and signature |
| Persistence | SQLite verdict history with configurable age-based retention |
| Stateful memory | Content-plus-ruleset fingerprint, acknowledgement TTL, automatic invalidation |
| Notification | ntfy for high and critical verdicts |
| Threat response | Deterministic log-pattern detection and operator-approved CrowdSec ban |
| Runbooks | Local Markdown ingestion, local embeddings, whole-document ChromaDB retrieval, and advisory answers conditioned on retrieved text with source titles |
| User interface | Authenticated single-page dashboard with status, history, threats, runbooks, and integration state |
| Security controls | Signed sessions, rate limiting, security headers, audit log, escaped dynamic dashboard content |
| Delivery | Docker Compose, Terraform for GCP, and GitHub Actions build/test/deploy workflows |
| Test evidence | 180 passing source-scoped tests; 89% overall line coverage across 1,655 statements with 190 missed, measured on 29 August 2026; six selected modules at 100%, orchestrator at 95%, and store at 94% |

The automated test result is evidence of selected implemented behaviour, not by itself evidence of production availability, attack resistance, or diagnostic accuracy. A separate frozen qwen2.5:3b benchmark measured 40.3% agreement with researcher-defined severity labels for one configuration; the labels were not independently adjudicated, so the result does not establish diagnostic truth or field efficacy. Live integration, fault-injection, security, population-level usability, and recovery testing remain separate release activities.

## 8. Core User Journeys

### 8.1 Review current infrastructure state

1. Operator signs in.
2. Dashboard loads the current verdict, age, and integration state.
3. Operator reads the summary.
4. Operator expands root cause and recommended action when more detail is needed.
5. Operator reviews recent check history for recurrence or escalation.

**Successful outcome:** The operator can identify severity, affected condition, evidence age, and next action without opening the raw telemetry tools first.

### 8.2 Acknowledge a known condition

1. Operator reviews an `ok` or `warning` verdict.
2. Operator selects **Mark known**, chooses an acknowledgement lifetime from 1 to 365 days, and may add a note through the API.
3. The system stores the acknowledgement against the verdict fingerprint.
4. Future matching low-risk verdicts are marked acknowledged and suppressed from the default view.
5. Changing the signature, prompt version, or model creates a different fingerprint and reopens evaluation.

**Safety constraint:** High and critical verdicts cannot be acknowledged or suppressed.

### 8.3 Respond to a detected threat

1. Operator opens the threat panel.
2. The API scans recent Loki lines using deterministic thresholds.
3. Operator reviews threat type, source IP, and evidence count.
4. Operator selects **Block IP** and confirms the action.
5. The server constructs and submits the CrowdSec decision, or reports dry-run mode.

**Successful outcome:** The result clearly states whether the decision was live, dry-run, or failed.

### 8.4 Consult a runbook

1. Runbook owner indexes or re-indexes the Markdown files under the configured runbook directory.
2. Operator asks an operational question.
3. The system retrieves relevant chunks and generates a bounded answer.
4. Dashboard displays the answer and source titles.

**Successful outcome:** The system says when no relevant runbook exists rather than inventing a procedure.

## 9. Functional Requirements

Priority uses MoSCoW: **Must**, **Should**, **Could**, and **Won't (current release)**.

### 9.1 Authentication and access

| ID | Requirement | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| FR-001 | Require authentication for dashboard and non-public API routes | Must | Unauthenticated browser requests redirect to login; API requests return 401 | Implemented |
| FR-002 | Rate-limit authentication attempts | Must | More than five login attempts per minute from one client are rejected | Implemented |
| FR-003 | End sessions safely | Must | Logout removes the session cookie; expired or invalid signatures are rejected | Implemented |
| FR-004 | Support individual users and roles | Could | Named users can be assigned viewer, operator, or administrator roles | Roadmap |

### 9.2 Telemetry collection and health analysis

| ID | Requirement | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| FR-010 | Collect logs from Loki when configured | Must | The cycle retrieves a bounded, recent, newest-first log window and records collection errors without crashing | Implemented |
| FR-011 | Collect metrics from Prometheus when configured | Must | CPU, available memory, root disk, and HTTP 5xx query results are represented separately | Implemented |
| FR-012 | Probe configured HTTP endpoints | Must | Each URL reports success/failure, status code where available, and latency | Implemented |
| FR-013 | Collect optional Docker evidence | Should | When explicitly enabled, monitored containers provide events and bounded diagnostics; when disabled, absence is not an incident | Implemented |
| FR-014 | Run analysis on a configurable schedule | Must | The default interval is 120 seconds and one failed cycle does not terminate the loop | Implemented |
| FR-015 | Produce a validated structured verdict | Must | Output contains an allowed severity, summary, root cause, recommended action, and signature; malformed provider output degrades to a warning | Implemented |
| FR-016 | Keep optional-integration absence out of incident reasoning | Must | Unconfigured Loki, Prometheus, HTTP, or Docker sources are not described as failed infrastructure | Implemented |
| FR-017 | Show stale-agent state | Must | Dashboard marks data stale after three configured heartbeat intervals without a verdict | Implemented |

### 9.3 Verdict history, memory, and notification

| ID | Requirement | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| FR-020 | Persist verdict history | Must | Each cycle stores timestamp, severity, summary, structured payload, signature, and fingerprint | Implemented |
| FR-021 | Retain history for a configurable period | Must | Records older than `VERDICT_RETENTION_DAYS` are removed during normal writes | Implemented |
| FR-022 | Notify on severe verdicts | Must | High and critical verdicts attempt ntfy delivery; lower severities do not | Implemented |
| FR-023 | Acknowledge a known low-risk condition | Must | An authenticated operator can acknowledge an existing `ok` or `warning` fingerprint with a note and TTL | Implemented |
| FR-024 | Automatically invalidate stale memory | Must | A changed signature, prompt version, model, or expired TTL no longer matches the old acknowledgement | Implemented |
| FR-025 | Prevent suppression of severe conditions | Must | High and critical acknowledgement requests return a conflict and remain visible | Implemented |
| FR-026 | Reverse an acknowledgement | Must | An authenticated operator can unacknowledge a fingerprint and matching verdicts return to normal display | Implemented |

### 9.4 Threat detection and response

| ID | Requirement | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| FR-030 | Detect supported threat patterns in Loki logs | Must | HTTP authentication failures, SSH failures, and port-scan indicators are counted per source IP against documented thresholds | Implemented |
| FR-031 | Show evidence before an enforcement action | Must | Threat card identifies pattern, IP, occurrence count, and description | Implemented |
| FR-032 | Require operator approval for IP blocking | Must | No CrowdSec decision is submitted merely because a threat was detected | Implemented |
| FR-033 | Provide safe dry-run behavior | Must | With no CrowdSec URL, the API returns a successful dry-run result and performs no ban | Implemented |
| FR-034 | Validate a selected threat and prevent repeated duplicate bans | Must | Type/IP is policy-valid and present in a fresh server-side detection; an active equivalent CrowdSec decision is not duplicated | Partially implemented: type/IP policy validation and fresh server-derived matching are tested; active-decision deduplication remains a production blocker |

### 9.5 Runbook assistant

| ID | Requirement | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| FR-040 | Index local Markdown runbooks | Must | Authenticated re-index synchronises changed and deleted runbooks without duplicates, returns the active document count, and reports refresh failures | Implemented |
| FR-041 | Condition advisory answers on retrieved runbooks | Must | Up to four whole retrieved documents and the question are bounded as untrusted data; no claim of factual support is inferred from retrieval alone | Implemented; answer-support validation remains an evaluation gap |
| FR-042 | Display answer sources | Should | Each response includes retrieved runbook source titles | Implemented |
| FR-043 | Show index freshness and last successful index result | Should | Dashboard shows indexed-document count, timestamp, and last error | Not implemented |

### 9.6 Dashboard and operations

| ID | Requirement | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| FR-050 | Present current state clearly | Must | First view shows severity, timestamp/age, summary, integration state, and stale warning | Implemented |
| FR-051 | Support history review | Must | Operator can view recent checks and hide acknowledged results | Implemented |
| FR-052 | Prevent untrusted text from executing in the browser | Must | LLM, log, user-question, and runbook text are rendered as escaped content | Implemented |
| FR-053 | Audit requests and operator actions | Must | Audit record includes UTC time, source, method, route, user, status, and latency | Implemented |
| FR-054 | Expose dependency readiness | Must | A readiness endpoint reports database and configured integration reachability separately from API liveness | Not implemented; production blocker |

## 10. Non-Functional Requirements

| ID | Category | Requirement and target | Current position |
|---|---|---|---|
| NFR-001 | Availability | API should recover automatically after process failure and expose liveness and readiness separately | Container restart exists; readiness incomplete |
| NFR-002 | Freshness | A completed verdict should normally be no older than three heartbeat intervals | Stale detection implemented; live SLO not measured |
| NFR-003 | Performance | Non-LLM dashboard API requests should achieve p95 under 500 ms on the target VM; runbook queries should return within 20 s | Targets not load-tested |
| NFR-004 | Reliability | One telemetry or LLM failure must not terminate the scheduler; failed analysis must create an explicit degraded warning | Implemented and unit-tested |
| NFR-005 | Security | Production traffic must use TLS; cookies must be `Secure`, `HttpOnly`, and `SameSite`; state-changing routes must have CSRF/origin protection | Partial; TLS and explicit CSRF/origin control are deployment blockers |
| NFR-006 | Secrets | Production credentials must come from a secret manager or workload identity, not a long-lived JSON key on disk | Not met for production; the demo workflow uses a deploy-time service-account secret and writes runtime values to a VM-local `.env` file; no key file is mounted in the application containers |
| NFR-007 | Privacy | Configurable redaction and allowlisting must remove secrets, tokens, personal data, and unnecessary log content before any external LLM call | Not implemented; production blocker for sensitive workloads |
| NFR-008 | Data protection | Verdict database and vector index require documented backup, restore, file permissions, and encryption-at-rest policy | Not documented/tested |
| NFR-009 | Auditability | Enforcement and acknowledgement actions must be attributable and retained; production audit logs should resist silent alteration | Attribution exists; tamper resistance does not |
| NFR-010 | Scalability | Current release supports one agent and one SQLite store; the UI should remain responsive while LLM work executes | Single-site scope documented; blocking API work moved to threads |
| NFR-011 | Deployability | Local startup must use one documented Compose command; cloud deployment must support rollback without avoidable downtime | Local path works; current cloud workflow runs `compose down` and lacks automatic rollback |
| NFR-012 | Maintainability | CI must run tests on pull requests; supervisor-targeted paths should reach 100% coverage and overall coverage should increase from the dated 66% baseline | Met for the 29 August source-scoped suite: 180 tests pass, six selected modules are at 100%, the orchestrator is at 95%, the store is at 94%, and overall coverage is 89%; live-integration coverage remains a separate gap |
| NFR-013 | Accessibility | Keyboard navigation, focus visibility, labels, contrast, and screen-reader semantics should meet WCAG 2.1 AA for core workflows | Not formally audited |
| NFR-014 | Cost control | Heartbeat, telemetry limits, prompt size, and model usage must be configurable; daily model spend must be measurable | Limits configurable; cost telemetry not implemented |

## 11. Data and AI Requirements

### 11.1 Data stores

- **SQLite `verdicts`:** timestamp, severity, summary, structured payload, signature, and fingerprint.
- **SQLite `acknowledgements`:** fingerprint, signature, original severity/summary, operator note, operator identity, created time, and expiry.
- **ChromaDB:** locally embedded Markdown runbook content and metadata.
- **Audit log:** request/action records written to local storage.

### 11.2 Data classification concerns

Logs and raw LLM payloads can contain identifiers, internal hostnames, customer data, credentials, or security details. The current store retains raw LLM output and selected diagnostic context. Before production use, the deployment owner must define:

- which log labels and fields may be sent to the selected model API;
- redaction rules for secrets, tokens, email addresses, and personal data;
- regional data-processing and retention requirements;
- who may read verdict history, vector data, and audit logs;
- backup retention and deletion procedures.

### 11.3 AI guardrails

- The model receives only configured telemetry blocks and known-condition context.
- The model must return a bounded JSON schema.
- Severity is validated against a fixed allowlist.
- Missing integrations are excluded from the prompt.
- Provider failure produces a degraded warning rather than a healthy result.
- Runbook answers are instructed to use retrieved documents only.
- Threat detection does not rely on the LLM.
- Enforcement remains human-approved.

### 11.4 AI limitations

- A structured answer can still be factually wrong or incomplete.
- The canonical signature is model-generated when available; the measured 41.7% repeat-stability means dependable semantic identity is unresolved.
- Empty or misleading telemetry produces correspondingly weak conclusions.
- The current model is a single external provider dependency.
- The frozen benchmark measured 40.3% agreement with researcher-defined severity labels for one evaluated local-model configuration. The labels were not independently adjudicated; the result is inadequate for unattended triage and does not establish real-world diagnostic efficacy.

## 12. Security Model

### 12.1 Implemented controls

- Signed, time-limited session cookies.
- Constant-time credential comparison.
- Five login attempts per minute and 60 requests per minute per client.
- CSP and common security headers.
- HTML escaping for dynamic dashboard content.
- Audit logging of requests and authenticated user identity.
- No automatic CrowdSec enforcement.
- No suppression of high or critical verdicts.
- Docker monitoring is opt-in.

### 12.2 Known security gaps

- One environment-configured administrator; no RBAC, account lifecycle, or MFA.
- The deployment workflow authenticates with a long-lived Google service-account secret and writes runtime values to a VM-local `.env` file; the application containers do not mount the key.
- No explicit CSRF token/origin validation on state-changing routes.
- CSP permits inline scripts and styles.
- CrowdSec type/IP validation and fresh server-side threat matching are implemented; active-decision deduplication still requires hardening.
- Docker socket access grants powerful host visibility even when mounted read-only.
- Local audit logs are not tamper-evident.
- No application-level encryption for stored verdict payloads or runbook vectors.
- `/health` confirms API liveness only, not dependency readiness.

## 13. Deployment and Operating Model

### 13.1 Current topology

- One API container on port 8080.
- One independent agent container.
- Shared SQLite volume.
- ChromaDB persistent volume mounted by the API.
- Runtime configuration supplied to both containers from the local `.env` file; no credential directory is mounted.
- Optional Docker socket mounted into the agent.
- External Loki, Prometheus, the selected model API, ntfy, CrowdSec, and probe targets.

### 13.2 Required production topology

- TLS-terminating reverse proxy or managed load balancer.
- API port restricted to approved networks or VPN where appropriate.
- Workload identity or managed secret delivery.
- Persistent-volume backup and tested restore procedure.
- Monitoring for the API, agent heartbeat, database growth, external dependency failures, and notification delivery.
- Deployment rollback that does not call `docker compose down` before replacement health is confirmed.

### 13.3 Operator runbook minimum

The production owner must document how to:

1. verify agent and API health;
2. rotate credentials and the session secret;
3. restore SQLite and Chroma data;
4. disable CrowdSec integration immediately;
5. disable Docker monitoring and remove the socket mount;
6. inspect failed model API, Loki, Prometheus, and ntfy calls;
7. roll back an application deployment;
8. export and retain audit records.

## 14. Success Metrics and Evaluation Plan

### 14.1 Product metrics

| Metric | Definition | Pilot target |
|---|---|---|
| Verdict availability | Completed cycles / scheduled cycles | >= 98% excluding planned maintenance |
| Verdict freshness | Time from expected heartbeat to stored verdict | p95 <= 3 heartbeat intervals |
| Scenario severity accuracy | Correct severity against a labelled fault-injection set | >= 85% |
| Action usefulness | Operator ratings of recommended action as useful or very useful | >= 80% |
| False severe-alert rate | High/critical verdicts during labelled healthy scenarios | <= 5% |
| Duplicate-noise reduction | Repeated acknowledged warnings hidden from default view | >= 80% without hiding severe transitions |
| Memory invalidation correctness | Changed condition/ruleset reopens after acknowledgement | 100% in test scenarios |
| Threat detection precision | Confirmed supported threats / displayed supported threats | >= 90% in controlled replay |
| Enforcement safety | CrowdSec actions made without operator confirmation | 0 |
| Runbook answer support | Answers fully supported by displayed sources under a retained independent item-level rubric | >= 90% on a labelled question set |
| Notification delivery | Successful high/critical ntfy requests | >= 99% when provider is available |
| Usability | System Usability Scale score from 3-5 representative users | >= 70 |
| Model cost | Daily and per-verdict inference cost | Measured and accepted before production |

### 14.2 Required evaluation exercises

1. **Healthy baseline:** Run at least 24 hours with normal traffic and label false alerts.
2. **Fault injection:** Exercise endpoint down, 5xx spike, database timeout logs, memory pressure, disk pressure, and container unhealthy/restart scenarios.
3. **Dependency failures:** Disconnect Loki, Prometheus, the selected model API, ntfy, and CrowdSec independently.
4. **Memory test:** Repeat a warning, acknowledge it, verify suppression, alter the condition, and verify reopening.
5. **Threat replay:** Replay supported HTTP, SSH, and scan patterns plus benign lookalikes; review precision.
6. **Runbook evaluation:** Use at least 20 answerable and 10 unanswerable questions with expected sources.
7. **Security review:** Test authentication, rate limits, session behavior, CSRF/origin policy, payload validation, secret leakage, and Docker-socket exposure.
8. **Recovery test:** Restore verdict and runbook data onto a clean host and measure recovery time.
9. **Usability study:** Observe 3-5 representative users completing status review, acknowledgement, threat dry-run, and runbook-query tasks.
10. **30-day controlled pilot:** Compare manual triage time, alert volume, and operator feedback with the pre-pilot baseline.

## 15. Release Readiness

### 15.1 Current assessment

| Area | Assessment | Evidence or gap |
|---|---|---|
| Core monitoring workflow | Functional | Implemented collectors, orchestrator, persistence, dashboard |
| Stateful memory | Functional | Fingerprint/TTL logic and severe-alert protection are tested |
| Automated tests | Strong source-scoped coverage; live integration still limited | 180 tests pass; 89% total coverage across 1,655 statements with 190 missed; six selected modules are at 100%, orchestrator is at 95%, and store is at 94%; external dependencies remain mocked in the controlled suite |
| User experience | Descriptive SUS evidence only | Ten complete convenience-sample SUS responses support favourable perceived usability in that group only. Practitioner role reports are qualitative material; their aggregate scores and kappas are excluded because assessor-by-item ratings are unavailable. Accessibility testing remains pending. |
| Security | Suitable for local/staging pilot | Important production controls remain incomplete |
| Operational resilience | Prototype level | Single host, liveness-only health, no tested backup/restore or automatic rollback |
| AI quality | Frozen single-configuration benchmark completed; operational validity unresolved | 40.3% researcher-label agreement and macro-F1 0.383 reject unattended triage for the evaluated qwen2.5:3b configuration; no independent gold-label adjudication or long-running field pilot has been completed |
| Compliance readiness | Not established | Data classification, redaction, audit retention, and governance pending |

### 15.2 P0 gates before a production pilot

- P0-01: Put the dashboard behind TLS and set `SESSION_COOKIE_SECURE=1`.
- P0-02: Add CSRF tokens or strict origin validation to all state-changing routes.
- P0-03: Replace the deploy-time long-lived service-account secret and VM-local `.env` materialisation with workload identity and managed secrets; no application-container key mount exists in the current demo.
- P0-04: Add telemetry redaction/allowlisting before LLM and persistence boundaries.
- P0-05: Add active CrowdSec-decision lookup/deduplication; type/IP validation and fresh server-side threat matching are already implemented.
- P0-06: Add a dependency-aware readiness endpoint and monitor agent heartbeat externally.
- P0-07: Implement and test SQLite/Chroma backup and restore.
- P0-08: Replace `compose down` deployment with health-checked replacement and documented rollback.
- P0-09: Run live end-to-end tests against representative Loki, Prometheus, model API, ntfy, and CrowdSec services.
- P0-10: Complete the labelled fault-injection and security evaluation in Section 14.

### 15.3 P1 gates before general single-site production use

- Add named user accounts, RBAC, and preferably OIDC/MFA.
- Self-host fonts and remove unnecessary inline CSP allowances.
- Add runbook-index freshness and failure visibility.
- Add cost, token, cycle-duration, and collector-health metrics.
- Add tamper-resistant central audit export.
- Perform accessibility testing and remediate core WCAG issues.
- Raise overall automated coverage, prioritising provider clients, Docker, notification, and RAG integration paths.

## 16. Roadmap

### Phase 1: Controlled operational pilot

- Complete all P0 gates.
- Deploy against one non-critical application.
- Run the fault-injection suite and 30-day pilot.
- Establish real baselines for accuracy, triage time, false alerts, cost, and operator usefulness.

### Phase 2: Reliable single-site production

- Complete P1 security, identity, audit, observability, and accessibility work.
- Add tested backup/restore and health-checked rollback.
- Calibrate thresholds and prompts from pilot evidence.

### Phase 3: Broader integrations

- Support additional notification channels and runbook sources.
- Add configurable PromQL and LogQL signal packs.
- Add distributed tracing where a justified use case exists.
- Add explicit feedback on verdict correctness and action usefulness.

### Phase 4: Multi-site and advanced operations

- Replace the shared single-host model with authenticated agents and a central control plane.
- Move from SQLite to a managed relational database when concurrent users or multiple agents require it.
- Add tenant boundaries, fleet inventory, RBAC, and enterprise SSO.
- Evaluate policy-controlled remediation only after diagnostic accuracy and safety targets have been met.

## 17. Risks and Mitigations

| Risk | Impact | Current mitigation | Required next action |
|---|---|---|---|
| LLM gives a plausible but wrong diagnosis | Incorrect operator action | Bounded prompt, strict five-field schema, evidence-focused output, human review, and a frozen benchmark showing only 40.3% agreement with researcher-defined labels for one configuration | Add independent label adjudication, extend evaluation across models and live fault scenarios, and add evidence links in the UI |
| Sensitive logs leave the environment | Privacy or compliance breach | Self-hosted control plane; limited telemetry window | Redaction/allowlist and formal data policy |
| Operator acknowledgement hides a changed fault | Missed incident | Fingerprint includes condition and ruleset; severe verdicts cannot be suppressed; TTL | Measure signature stability and add deterministic signatures for key signals |
| Threat detector blocks a legitimate IP | Availability/security harm | Human confirmation, dry-run mode, IP policy validation, and fresh server-side evidence matching | Add an explicit allowlist, active-decision deduplication, and stronger auditable confirmation |
| Monitoring agent silently stops | False sense of safety | Dashboard stale banner | External heartbeat alert and dependency readiness |
| Docker socket is abused | Host compromise | Feature is opt-in; mount marked read-only | Remove mount when disabled; use a constrained proxy where enabled |
| Model API or telemetry service is unavailable | Degraded analysis | Tool errors represented; loop continues | Dependency SLOs, retry/backoff, readiness, and clear UI errors |
| SQLite corruption or host loss | Loss of history and memory | Persistent volume | Automated backup and tested restore |
| Deployment causes avoidable downtime | Monitoring blind spot | Containers restart automatically | Health-checked update and rollback strategy |
| Operating cost grows unexpectedly | Budget impact | 120-second interval and bounded inputs | Token/cost metering, budget alerts, adaptive analysis policy |

## 18. Dependencies and Assumptions

### Required for the core product

- Python 3.11 container runtime.
- An API key for Gemini, Anthropic, or OpenAI, unless local Ollama is selected.
- Valid Google authentication configured for the containers.
- At least one useful telemetry input: Loki, Prometheus, or HTTP probes.
- Persistent storage for SQLite.
- A strong session secret and non-default administrator credentials.

### Optional

- Docker Engine access for container monitoring.
- ntfy topic for notifications.
- Local Markdown runbooks and a Chroma volume for runbook assistance.
- CrowdSec Local API for live IP bans.
- Terraform and GCE for the provided cloud deployment path.

### Assumptions

- The deployment owner has permission to collect and process the configured telemetry.
- Network connectivity and firewall rules permit the configured integrations.
- Operators understand that verdicts are recommendations, not proof of root cause.
- Runbooks are reviewed and maintained by their owners.
- The target deployment is one team and one operational environment until the multi-site roadmap is implemented.

## 19. API Surface Summary

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | API liveness |
| GET/POST | `/login` | Authentication |
| GET | `/logout` | End session |
| GET | `/` | Dashboard |
| GET | `/status` | Latest verdict, staleness, and memory state |
| GET | `/alerts` | Recent verdict history |
| GET | `/api/config` | Boolean integration status and agent configuration |
| GET | `/api/agent/mode` | Active reasoning mode and model |
| POST | `/api/verdicts/ack` | Acknowledge an existing low-risk fingerprint |
| POST | `/api/verdicts/unack` | Remove an acknowledgement |
| GET | `/api/acks` | List active acknowledgements |
| GET | `/api/threats` | Scan recent Loki logs for supported threat patterns |
| POST | `/api/threats/apply` | Apply or dry-run an operator-approved CrowdSec decision |
| POST | `/api/runbooks/index` | Re-index local Markdown runbooks |
| POST | `/api/runbooks/query` | Ask the runbook assistant for an advisory answer conditioned on retrieved text with source titles |

## 20. Definition of Done

The current product is considered ready for a **controlled pilot** when:

1. the current source-scoped suite (180 tests at the 29 August snapshot) still passes in CI, with any later count reconciled before release;
2. all P0 release gates in Section 15.2 are complete;
3. the live integration and fault-injection exercises pass with recorded evidence;
4. no high or critical scenario can be hidden through acknowledgement;
5. backup and restore are demonstrated on a clean host;
6. the deployment owner approves measured model cost and data handling;
7. 3-5 representative users complete the core tasks without a blocking usability issue;
8. an operator runbook and rollback procedure are available;
9. remaining known risks have named owners and accepted dates.

The product is considered ready for **general single-site production use** only after the P1 gates are complete and the 30-day pilot meets the targets in Section 14.
