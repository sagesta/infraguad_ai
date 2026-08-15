# InfraGuard Pro — Project Context

This document provides a complete picture of the project: what it is, where it stands, key decisions made, and how the codebase relates to the master's project submission.

## Identity

| Field | Value |
|-------|-------|
| **Project title** | Design and Development of an LLM-Based Autonomous Security Remediation System for Cloud-Native CI/CD Pipelines |
| **Platform name** | InfraGuard Pro (evolved from InfraGuard AI) |
| **Programme** | Professional Master of Information Technology (MIT), Miva Open University Abuja |
| **Submission** | May 2026 |
| **Repository** | This repo (`infraguad_ai/`) |
| **Report** | `docs/masters_project/InfraGuard_Pro_Masters_Project.docx` |

## What InfraGuard Pro Is

InfraGuard Pro is a self-hosted DevSecOps platform with two complementary capabilities:

1. **Runtime Observability Agent** (built, operational) — continuously monitors infrastructure via Loki, Prometheus, Docker, and HTTP probes; uses LLM-driven reasoning to diagnose issues and trigger alerts.

2. **Autonomous Security Remediation Engine** (described in project, implementation in progress) — ingests scanner output (SARIF), enriches findings with RAG context, generates structured patch proposals via pluggable LLM providers, routes them through a three-mode policy engine, opens pull requests, and validates fixes in a closed feedback loop.

The master's project positions capability (2) as the headline contribution while capability (1) serves as the runtime validation surface for the closed-loop pipeline.

## Architecture Overview

```
                    +------------------+
                    |  CI/CD Pipeline  |
                    |  (GitHub Actions)|
                    +--------+---------+
                             |
                    SARIF scanner output
                             |
                             v
+----------------------------+----------------------------+
|              CENTRAL CONTROL PLANE                      |
|                                                         |
|  +---------------+  +----------------+  +------------+  |
|  | SARIF Adapter  |  | Remediation    |  | Policy     |  |
|  | (ingestion)    |->| Engine         |->| Engine     |  |
|  +---------------+  | (LLM + RAG)    |  | (3 modes)  |  |
|                      +----------------+  +------+-----+  |
|                                                 |        |
|  +---------------+  +----------------+  +-------v-----+  |
|  | LLM Provider  |  | Multi-Source   |  | Git Provider|  |
|  | Abstraction   |  | RAG Corpus     |  | Adapter     |  |
|  | (6 backends)  |  | (CVE, runbooks)|  | (PR creation|  |
|  +---------------+  +----------------+  +-------------+  |
|                                                          |
|  +---------------+  +----------------+  +-------------+  |
|  | Audit Log     |  | Closed-Loop    |  | SvelteKit   |  |
|  | (hash-chain)  |  | Validator      |  | Dashboard   |  |
|  +---------------+  +----------------+  +-------------+  |
+----------------------------+----------------------------+
                             |
              Heartbeat / WebSocket
                             |
               +-------------+-------------+
               |        SATELLITE(s)       |
               |  per-server lightweight   |
               |  agent with local SQLite  |
               +---------------------------+
```

## Current Codebase State

### What Is Built and Working

| Component | Location | Status |
|-----------|----------|--------|
| Agent heartbeat loop | `agent/main.py` | Working |
| LangGraph orchestrator (collect/analyze/decide/notify) | `agent/orchestrator.py` | Working |
| Vertex AI / Gemini integration | `agent/llm/vertex.py` | Working |
| LangChain multi-tool reasoning | `agent/llm/langchain_agent.py` | Working |
| Prompt assembly | `agent/llm/prompts.py` | Working |
| ChromaDB vector store | `agent/rag/vector_store.py` | Working |
| Notion runbook loader | `agent/rag/notion_loader.py` | Working |
| RAG query interface | `agent/rag/runbook_agent.py` | Working |
| Prometheus metrics collection | `agent/tools/prometheus.py` | Working |
| Loki log collection | `agent/tools/loki.py` | Working |
| Docker events/stats/logs | `agent/tools/docker_*.py` | Working |
| HTTP endpoint probing | `agent/tools/http_probe.py` | Working |
| CrowdSec threat response | `agent/tools/threat_response.py` | Working |
| ntfy.sh notifications | `agent/tools/notify.py` | Working |
| FastAPI API server | `api/main.py` | Working |
| Cookie-based authentication | `api/auth.py` | Working |
| SQLite verdict persistence | `api/store.py` | Working |
| Security headers middleware | `api/middleware/security.py` | Working |
| Audit logging middleware | `api/middleware/audit.py` | Working |
| Rate limiting middleware | `api/middleware/rate_limit.py` | Working |
| HTML dashboard (dark mode) | `dashboard/index.html` | Working |
| Docker Compose (2 services) | `docker-compose.yml` | Working |
| Terraform (GCE + Artifact Registry) | `terraform/` | Working |
| GitHub Actions CI/CD | `.github/workflows/` | Working |
| Promtail log shipping | `promtail/` | Working |
| Test suite (pytest + respx) | `tests/` | Working |

### What Is Described in the Master's Project but Not Yet Implemented

These are the "InfraGuard Pro" extensions documented in the master's project report. They are the features that differentiate the master's submission from the base platform.

| Feature | Priority | Complexity | Notes |
|---------|----------|------------|-------|
| SARIF v2.1.0 ingestion pipeline | High | Medium | Parse multi-scanner SARIF output into normalised finding records |
| Multi-LLM provider abstraction | High | Medium | Strategy pattern: OpenAI, Anthropic, Kimi, Ollama, LM Studio alongside existing Vertex AI |
| Autonomous Remediation Engine | High | High | 8-step pipeline: ingest, enrich, retrieve, generate, classify, route, commit, validate |
| Three-mode policy engine | High | Medium | YAML-configurable: recommend-only, human-approval, autonomous-low-risk |
| Git provider adapter (PR creation) | High | Medium | GitHub/GitLab API wrapper for opening PRs with generated patches |
| Closed-loop validator | Medium | High | Re-run scanner post-patch + runtime telemetry regression check |
| Multi-source RAG expansion | Medium | Medium | Local markdown, uploaded files, historical fix outcomes beyond Notion |
| Satellite agent architecture | Medium | High | Lightweight per-server agents with local SQLite + heartbeat to control plane |
| SvelteKit dashboard | Medium | High | Modern replacement for the vanilla HTML dashboard |
| PostgreSQL for central control plane | Medium | Medium | Replace SQLite for multi-user, multi-satellite concurrency |
| Tamper-evident audit log | Low | Medium | SHA-256 hash-chained append-only log entries |
| Expanded REST API (26+ endpoints) | Medium | Medium | Remediation, policy, satellite, audit, provider management endpoints |
| 150-finding evaluation benchmark | Medium | Medium | Reproducible test harness with real + synthetic findings across providers |

## Key Decisions

1. **Honest academic framing**: Chapter 5 of the master's project separates measured apparatus-level results (test coverage, self-scanning) from the proposed 150-finding evaluation protocol. Projected outcomes are clearly labelled as forecasts, not measurements.

2. **LLM provider abstraction via strategy pattern**: Each provider implements a common `LLMProvider` abstract base class with `generate_patch()`, `health_check()`, and `estimate_cost()`. A `ProviderRegistry` manages runtime selection and hot-swap.

3. **Three-mode policy engine**: Findings are routed based on severity, confidence, and scanner class. Autonomous mode is restricted to low-risk, high-confidence findings only. The policy is configurable per-organisation via YAML.

4. **SARIF as the universal scanner interchange**: All scanner output is normalised to SARIF v2.1.0 before entering the remediation pipeline. This avoids per-scanner parsers.

5. **Closed-loop validation**: A patch is not considered "fixed" until the originating scanner re-runs clean AND runtime telemetry shows no regressions for a configurable observation window.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| API framework | FastAPI |
| Agent framework | LangGraph + LangChain |
| LLM (current) | Google Vertex AI (Gemini 2.5 Flash) |
| LLM (planned) | OpenAI GPT-4o, Anthropic Claude, Moonshot Kimi, Ollama, LM Studio |
| Vector store | ChromaDB |
| Database (current) | SQLite via aiosqlite |
| Database (planned) | PostgreSQL (central), SQLite (satellite) |
| Dashboard (current) | Vanilla HTML + JS |
| Dashboard (planned) | SvelteKit 5 + Tailwind CSS 4 |
| Container runtime | Docker + Docker Compose |
| IaC | Terraform (GCP) |
| CI/CD | GitHub Actions |
| Metrics | Prometheus |
| Logs | Grafana Loki + Promtail |
| Threat detection | CrowdSec |
| Notifications | ntfy.sh |

## File Layout

```
infraguad_ai/
  agent/                    # Autonomous agent
    llm/                    # LLM integrations (vertex.py, langchain_agent.py, prompts.py)
    rag/                    # RAG system (vector_store.py, notion_loader.py, runbook_agent.py)
    tools/                  # Data collectors + actions (prometheus, loki, docker_*, http_probe, notify, threat_response)
    main.py                 # Heartbeat entry point
    orchestrator.py         # LangGraph state machine
    Dockerfile
  api/                      # FastAPI web server
    middleware/              # Security headers, audit logging, rate limiting
    main.py                 # Routes and app factory
    auth.py                 # Session management
    store.py                # SQLite persistence
    Dockerfile
  dashboard/                # Web UI
    index.html              # Main dashboard (dark mode)
    login.html              # Login page
  tests/                    # pytest suite
  terraform/                # GCP infrastructure-as-code
  promtail/                 # Log shipping config
  docs/masters_project/     # Master's report generator
    content/                # Chapters 00-08 (JS modules)
    figures/                # 14 PNG diagrams (matplotlib)
    helpers.js              # Shared docx formatting
    build.js                # Assembles and writes .docx
  .github/workflows/        # CI/CD pipelines
  .env.example              # Environment variable template
  docker-compose.yml        # 2-service stack (api + agent)
  requirements.txt          # Python dependencies
  CONTEXT.md                # Technical assistant context (existing)
  README.md                 # User-facing README
  prd.md                    # Product requirements document
  system_architecture.md    # Architecture with Mermaid diagram
```

## Relationship Between Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| `PROJECT_CONTEXT.md` (this file) | Complete project state and decisions | Developer / supervisor |
| `CONTEXT.md` | Technical assistant context for LLM tools | AI coding assistants |
| `README.md` | Setup and usage | Developers / evaluators |
| `RUNNING_GUIDE.md` | Step-by-step demo and sampling guide | Supervisor / examiner |
| `TODO.md` | Remaining implementation work | Developer |
| `prd.md` | Product requirements | Stakeholders |
| `system_architecture.md` | Architecture diagram and rationale | Technical reviewers |
| `docs/masters_project/` | Full academic report (25k+ words) | University submission |
