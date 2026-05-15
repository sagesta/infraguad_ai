# InfraGuard Pro — Implementation TODO

This file tracks the remaining work to bring the codebase from its current state (InfraGuard AI) to the full InfraGuard Pro vision described in the master's project report. Items are grouped by priority and roughly ordered by dependency.

---

## Legend

- **[CRITICAL]** — Must be done for the project to match the master's report claims
- **[HIGH]** — Strongly recommended; referenced in the report
- **[MEDIUM]** — Enhances the platform; described but not load-bearing for the submission
- **[LOW]** — Nice-to-have; mentioned in future work

---

## Phase 1: Core Remediation Pipeline (CRITICAL)

These features form the backbone of the master's project contribution. Without them, the report describes capabilities that don't exist in the code.

### 1.1 SARIF Ingestion Adapter
- [ ] Create `agent/sarif/adapter.py` — parse SARIF v2.1.0 JSON into normalised finding records
- [ ] Support multi-run SARIF files (multiple scanners in one file)
- [ ] Extract: rule ID, severity, message, file path, line range, CWE ID, fingerprint
- [ ] Map SARIF severity levels (`error`, `warning`, `note`) to internal severity scale
- [ ] Add API endpoint `POST /api/sarif/ingest` to accept SARIF uploads
- [ ] Add API endpoint `POST /api/sarif/webhook` for CI/CD pipeline callbacks
- [ ] Write unit tests with sample SARIF from Trivy, Semgrep, and CodeQL
- **Reference**: Report Section 4.2.3, Table 4.2

### 1.2 Multi-LLM Provider Abstraction
- [ ] Create `agent/llm/base.py` — abstract base class `LLMProvider` with methods:
  - `generate_patch(finding, context) -> PatchProposal`
  - `health_check() -> ProviderHealth`
  - `estimate_cost(tokens) -> float`
- [ ] Refactor `agent/llm/vertex.py` to implement `LLMProvider`
- [ ] Create `agent/llm/openai_provider.py` — OpenAI GPT-4o
- [ ] Create `agent/llm/anthropic_provider.py` — Anthropic Claude
- [ ] Create `agent/llm/kimi_provider.py` — Moonshot Kimi
- [ ] Create `agent/llm/ollama_provider.py` — Ollama (local, zero-cost)
- [ ] Create `agent/llm/lmstudio_provider.py` — LM Studio (local)
- [ ] Create `agent/llm/registry.py` — `ProviderRegistry` for runtime selection, fallback, hot-swap
- [ ] Create `agent/llm/health_monitor.py` — `ProviderHealthMonitor` with periodic health checks
- [ ] Add API endpoint `GET /api/providers` to list available providers and their status
- [ ] Add API endpoint `POST /api/providers/{name}/select` to switch active provider
- [ ] Add env vars: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `KIMI_API_KEY`, `OLLAMA_URL`, `LMSTUDIO_URL`
- [ ] Write tests for each provider (mock-based)
- **Reference**: Report Section 4.2.2, Figure 4.2, Table 3.3

### 1.3 Remediation Engine
- [ ] Create `agent/remediation/engine.py` — 8-step pipeline:
  1. Ingest (SARIF finding)
  2. Enrich (CVE lookup, CWE context)
  3. Retrieve (RAG: runbooks, historical fixes, CVE data)
  4. Generate (LLM patch proposal with structured output)
  5. Classify (policy engine categorisation)
  6. Route (based on policy mode)
  7. Commit (Git PR via provider adapter)
  8. Validate (closed-loop scanner re-run)
- [ ] Define `PatchProposal` data model: diff, confidence score, citation chain, policy classification
- [ ] Define `RemediationRecord` data model for persistence and audit
- [ ] Integrate with the LLM provider abstraction
- [ ] Add API endpoints:
  - `POST /api/remediation/trigger` — manual trigger for a finding
  - `GET /api/remediation/{id}` — get remediation status
  - `GET /api/remediation/queue` — list pending remediations
  - `POST /api/remediation/{id}/approve` — human approval
  - `POST /api/remediation/{id}/reject` — human rejection
- [ ] Write integration tests for the full pipeline (mocked LLM + Git)
- **Reference**: Report Section 4.2.4, Figure 3.3, Figure 3.5

### 1.4 Three-Mode Policy Engine
- [ ] Create `agent/policy/engine.py` — rule-based classifier
- [ ] Create `agent/policy/config.py` — YAML configuration loader
- [ ] Create default policy YAML: `config/policy.yaml`
- [ ] Implement three modes:
  - **recommend-only**: generate patch, log it, do nothing
  - **human-approval**: generate patch, create PR as draft, wait for human approval
  - **autonomous-low-risk**: generate patch, create PR, auto-merge if confidence > threshold AND severity < threshold
- [ ] Classification rules: severity, confidence score, scanner class, CWE category
- [ ] Add API endpoints:
  - `GET /api/policy` — get current policy config
  - `PUT /api/policy` — update policy config
  - `GET /api/policy/modes` — list available modes
- [ ] Write tests for each mode and edge cases
- **Reference**: Report Section 4.2.5

### 1.5 Git Provider Adapter
- [ ] Create `agent/git/adapter.py` — abstract base for Git operations
- [ ] Create `agent/git/github.py` — GitHub API (PyGithub or httpx):
  - Create branch
  - Commit file changes
  - Open pull request (regular or draft)
  - Add reviewers
  - Merge PR
  - Read PR status
- [ ] Create `agent/git/gitlab.py` — GitLab API (python-gitlab or httpx)
- [ ] Add env vars: `GITHUB_TOKEN`, `GITHUB_REPO`, `GITLAB_TOKEN`, `GITLAB_PROJECT_ID`
- [ ] Write tests with mock responses
- **Reference**: Report Section 4.2.6

---

## Phase 2: Validation and Audit (HIGH)

### 2.1 Closed-Loop Validator
- [ ] Create `agent/validation/validator.py`:
  - Re-run originating scanner after patch is merged
  - Parse new SARIF output to confirm finding is resolved
  - Monitor runtime telemetry (Prometheus, Loki) for regressions during observation window
  - Record outcome (pass/fail/inconclusive) and feed back into RAG corpus
- [ ] Configurable observation window (default: 30 minutes)
- [ ] Add API endpoint `GET /api/remediation/{id}/validation` — validation status
- **Reference**: Report Section 4.2.8

### 2.2 Tamper-Evident Audit Log
- [ ] Create `agent/audit/hash_chain.py`:
  - Each audit entry includes SHA-256 hash of the previous entry
  - Entries are append-only
  - Verification function to check chain integrity
- [ ] Migrate from `api/middleware/audit.py` (JSON file) to database-backed hash chain
- [ ] Add API endpoint `GET /api/audit` — paginated audit log
- [ ] Add API endpoint `GET /api/audit/verify` — verify chain integrity
- **Reference**: Report Section 4.3.1, Appendix B

### 2.3 Multi-Source RAG Expansion
- [ ] Add markdown file loader to `agent/rag/` — index local `.md` runbooks
- [ ] Add file upload loader — accept uploaded docs via API
- [ ] Add historical fix loader — index past successful remediations as RAG context
- [ ] Add CVE data loader — fetch and index CVE descriptions from NVD
- [ ] Unify all loaders under a common `CorpusLoader` interface
- [ ] Add API endpoint `POST /api/rag/upload` — upload a runbook file
- [ ] Add API endpoint `GET /api/rag/sources` — list indexed sources
- **Reference**: Report Section 4.2.7

---

## Phase 3: Multi-Server and Dashboard (MEDIUM)

### 3.1 Satellite Agent Architecture
- [ ] Create `satellite/` directory with lightweight agent:
  - Local SARIF collection and forwarding
  - Local SQLite buffering for offline resilience
  - Heartbeat to central control plane
  - Telemetry forwarding (Prometheus, Loki)
- [ ] Create `satellite/Dockerfile`
- [ ] Add control plane registration endpoint `POST /api/satellites/register`
- [ ] Add satellite status endpoint `GET /api/satellites`
- [ ] Add satellite heartbeat endpoint `POST /api/satellites/{id}/heartbeat`
- [ ] Create `docker-compose.satellite.yml` for satellite deployment
- **Reference**: Report Section 4.2.9, Figure 3.2

### 3.2 SvelteKit Dashboard
- [ ] Scaffold SvelteKit 5 project in `dashboard-v2/`
- [ ] Implement pages:
  - Fleet overview (multi-server status cards)
  - Remediation queue (pending/approved/rejected)
  - Finding detail view (diff preview, confidence, citations)
  - Policy configuration editor
  - Provider management (health, usage, costs)
  - Audit log viewer
  - Runbook chat (existing RAG interface, modernised)
- [ ] Tailwind CSS 4 styling (dark mode default)
- [ ] WebSocket for real-time verdict updates
- [ ] Add `dashboard-v2/Dockerfile`
- [ ] Update `docker-compose.yml` to include dashboard service
- **Reference**: Report Section 4.2.10, Figure 4.3

### 3.3 PostgreSQL Migration
- [ ] Add PostgreSQL service to `docker-compose.yml`
- [ ] Create schema: `findings`, `remediations`, `verdicts`, `satellites`, `audit_log`, `policy_config`, `providers`
- [ ] Create `api/db.py` — async PostgreSQL client (asyncpg or SQLAlchemy async)
- [ ] Migrate `api/store.py` from SQLite to PostgreSQL
- [ ] Keep SQLite for satellite agents (local buffering)
- **Reference**: Report Section 3.4

### 3.4 Expanded API Endpoints
- [ ] Implement all 26+ endpoints listed in Table 4.2 of the report
- [ ] Add OpenAPI schema documentation
- [ ] Add API versioning (`/api/v1/...`)
- **Reference**: Report Table 4.2, Appendix A

---

## Phase 4: Evaluation and Testing (MEDIUM)

### 4.1 150-Finding Benchmark
- [ ] Create `benchmarks/` directory
- [ ] Curate 150 findings:
  - 90 from real scanner output (Trivy, Semgrep, CodeQL, Checkov, Gitleaks)
  - 60 synthetically injected with known-good patches
  - Distribution: 30 SAST, 30 SCA, 30 container, 30 IaC, 30 secrets
  - CVSS bands: 50 critical/high, 50 medium, 50 low
- [ ] Create `benchmarks/harness.py` — automated evaluation runner:
  - Run each finding through the remediation engine with each provider
  - Record: patch generated, accepted/rejected, time, tokens, cost
  - Compare against known-good patches (edit distance, AST diff)
- [ ] Create `benchmarks/results/` — output directory for results
- [ ] Add statistical analysis scripts (mean, std dev, confidence intervals)
- [ ] Replace illustrative projections in Chapter 5 with actual measurements
- **Reference**: Report Section 5.3

### 4.2 Security Self-Scanning
- [ ] Add Trivy container scanning to CI pipeline
- [ ] Add Semgrep SAST scanning to CI pipeline
- [ ] Add Gitleaks secret detection to CI pipeline
- [ ] Feed scanner output back into InfraGuard Pro's own remediation engine (eat your own dog food)
- **Reference**: Report Section 5.1.3

### 4.3 Adversarial Testing
- [ ] Create `tests/test_adversarial.py`:
  - Prompt injection via SARIF fields (rule descriptions, messages)
  - Prompt injection via runbook content
  - Policy bypass attempts (crafted confidence scores)
- [ ] Document results and mitigations
- **Reference**: Report Section 5.1.4

### 4.4 Expand Test Coverage
- [ ] Target 84%+ line coverage (matching report claims)
- [ ] Add tests for all new modules (SARIF, remediation, policy, git, validator, audit)
- [ ] Add integration tests for the full pipeline
- [ ] Add load tests for the API under concurrent requests
- **Reference**: Report Section 5.2.1

---

## Phase 5: Polish and Submission (LOW)

### 5.1 Documentation
- [ ] Update `README.md` with InfraGuard Pro features and setup
- [ ] Update `CONTEXT.md` with new modules and endpoints
- [ ] Update `system_architecture.md` with remediation pipeline
- [ ] Write API documentation (Swagger/OpenAPI)

### 5.2 Master's Report Finalisation
- [ ] Fill in `[NAME OF STUDENT]` and `[Matriculation Number]` in `docs/masters_project/content/00-prelim.js`
- [ ] Verify page numbers in Table of Contents match rendered output
- [ ] Run through Turnitin or equivalent plagiarism checker
- [ ] Verify all 45 references are accessible
- [ ] Get supervisor sign-off on literature review table
- [ ] Print test copy for formatting review

### 5.3 CI/CD Pipeline Updates
- [ ] Add security scanning steps to GitHub Actions
- [ ] Add benchmark execution to CI (on tag/release)
- [ ] Add dashboard build step (when SvelteKit is implemented)

### 5.4 Future Work (Post-Submission)
- [ ] Mobile-first operations companion (PWA)
- [ ] Ticketing system integration (Jira, Linear, Asana)
- [ ] Sharded control plane for large fleets
- [ ] Provider-aware confidence recalibration
- [ ] Multi-agent cooperation (retrieval + patch + policy agents)

---

## Implementation Priority Order

For the master's project submission, focus on this order:

1. **SARIF adapter + sample files** — proves scanner integration works
2. **LLM provider abstraction** — shows the multi-provider architecture is real
3. **Policy engine** — the three-mode system is a key differentiator
4. **Remediation engine** — ties everything together
5. **Git adapter** — PR creation completes the pipeline
6. **Audit hash chain** — compliance/trust angle
7. **Expanded tests** — backs up the 84% coverage claim
8. **150-finding benchmark** — converts projections to measurements

Items 1-6 can be demonstrated in human-approval mode even without a full SvelteKit dashboard — the existing API and HTML dashboard are sufficient for a supervisor demo. The SvelteKit dashboard and satellite architecture are valuable but not required for a defensible submission.
