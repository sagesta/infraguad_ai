# InfraGuard Pro — Running Guide

Step-by-step instructions for setting up, running, testing, and demonstrating the platform.

---

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Docker + Docker Compose | 24+ / v2+ | Containerised deployment |
| Node.js | 18+ | Master's project docx builder only |
| Git | 2.40+ | Version control |
| Model-provider API key | — | Gemini, Anthropic, or OpenAI inference |

Optional (for specific features):

| Requirement | Purpose |
|-------------|---------|
| DevPlanner Compose stack | Same-VPS metrics, logs, probes, and CrowdSec |
| Terraform | GCP infrastructure provisioning |

---

## 1. Local Development Setup

### 1.1 Clone and Install

```bash
git clone <repo-url> infraguard-ai
cd infraguard-ai

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\Activate.ps1     # Windows PowerShell

pip install -r requirements.txt
```

### 1.2 Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your values. The minimum required variables for a basic run:

```env
# Auth (pick any username/password for local use)
INFRAGUARD_USERNAME=admin
INFRAGUARD_PASSWORD=your-password
SECRET_KEY=any-random-string-32-chars

# Model provider
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-google-ai-studio-key
GEMINI_MODEL=gemini-3.6-flash

# Target container (name of the Docker container you want to monitor)
DEVPLANNER_CONTAINER_NAME=devplanner-api

# Same-VPS private Docker network and DevPlanner services
OBSERVABILITY_NETWORK=infraguard-observability
LOKI_URL=http://devplanner-loki:3100
PROMETHEUS_URL=http://devplanner-prometheus:9090
PROBE_URLS=http://devplanner-api:3001/health,http://devplanner-web:3000

# CrowdSec machine credentials; use the same values in DevPlanner
CROWDSEC_API_URL=http://devplanner-crowdsec:8080
CROWDSEC_MACHINE_ID=infraguard
CROWDSEC_MACHINE_PASSWORD=use-a-strong-random-password

# Notifications
NTFY_TOPIC=infraguard-test

# Database
DB_PATH=./verdicts.db

# Agent mode
USE_LANGCHAIN_AGENT=1
HEARTBEAT_INTERVAL_SECONDS=120
```

### 1.3 Model Credentials

Create a Gemini Developer API key in Google AI Studio, or select Anthropic or
OpenAI and set the corresponding provider key. No GCP service account, Vertex
IAM role, or Notion token is required. Local Markdown files under `runbooks/`
provide the retrieval corpus.

### 1.4 Run Without Docker (Development)

Open two terminals:

**Terminal 1 — API server:**
```bash
PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload
```

**Terminal 2 — Agent loop:**
```bash
PYTHONPATH=. python -m agent.main
```

On Windows PowerShell:
```powershell
$env:PYTHONPATH = "."
uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload
# (separate terminal)
$env:PYTHONPATH = "."
python -m agent.main
```

Access the dashboard at `http://localhost:8080`. Log in with the credentials from `.env`.

---

## 2. Docker Compose Deployment

### 2.1 Build and Run

Create the external network once, start DevPlanner, and then start InfraGuard:

```bash
docker network create infraguard-observability
docker compose up -d --build
```

Register InfraGuard's CrowdSec machine once from the DevPlanner directory using
the matching credentials in both `.env` files.

### 2.2 Verify

```bash
# Check services are running
docker compose ps

# Check API health
curl http://localhost:8080/health

# View agent logs (should see heartbeat cycles)
docker compose logs -f agent

# View API logs
docker compose logs -f api
```

### 2.3 Access Dashboard

Open `http://localhost:8080` in a browser. Log in with the `INFRAGUARD_USERNAME` / `INFRAGUARD_PASSWORD` from `.env`.

The dashboard shows:
- **Severity cards** — current system health verdict
- **Alerts table** — historical verdicts with timestamps
- **Threat detection panel** — CrowdSec-sourced threats
- **Runbook chat** — query your indexed runbooks via RAG

---

## 3. Running Tests

```bash
# Run the full test suite
PYTHONPATH=. pytest -v

# Run specific test files
PYTHONPATH=. pytest tests/test_agent.py -v
```
PYTHONPATH=. pytest tests/test_api.py -v
PYTHONPATH=. pytest tests/test_rag.py -v
PYTHONPATH=. pytest tests/test_threat_response.py -v
PYTHONPATH=. pytest tests/test_tools.py -v

# Run with coverage
PYTHONPATH=. pytest --cov=agent --cov=api --cov-report=term-missing
```

On Windows PowerShell:
```powershell
$env:PYTHONPATH = "."
pytest -v
```

The tests mock model-provider and telemetry HTTP calls, so they run without live infrastructure dependencies.

---

## 4. Indexing Runbooks (RAG)

Add Markdown files under `./runbooks` (subdirectories become categories), start
the API server, and trigger indexing:

```bash
# Via curl (requires an active session cookie)
curl -X POST http://localhost:8080/api/runbooks/index \
  -b "session=$(curl -s -c - http://localhost:8080/login \
    -d 'username=admin&password=your-password' | grep session | awk '{print $7}')"
```

You can also click **Re-index** in the authenticated dashboard.

Once indexed, query runbooks via the dashboard chat or:

```bash
curl -X POST http://localhost:8080/api/runbooks/query \
  -H "Content-Type: application/json" \
  -b "session=<your-session-cookie>" \
  -d '{"query": "how to restart the payment service"}'
```

---

## 5. Demonstration / Sampling Walkthrough

Use this sequence to demonstrate the platform to a supervisor or examiner.

### Step 1: Show the Architecture

Open `system_architecture.md` and walk through the Mermaid diagram. Key points:
- Telemetry flows in from Prometheus, Loki, Docker, and HTTP probes.
- LangGraph orchestrator coordinates the reasoning pipeline.
- Gemini, Anthropic, OpenAI, or Ollama provides LLM inference.
- ChromaDB and local Markdown runbooks provide retrieval context.
- CrowdSec provides threat detection and response.

### Step 2: Start the Stack

```bash
docker compose up -d --build
docker compose logs -f
```

Wait for the first heartbeat cycle (~60-120 seconds). You should see the agent log output showing:
- Data collection from available sources
- LLM inference (Gemini verdict)
- Verdict persistence
- Notification dispatch (if severity is high/critical)

### Step 3: Dashboard Demo

1. Open `http://localhost:8080` and log in.
2. Show the **severity cards** updating after each heartbeat.
3. Show the **alerts table** with historical verdicts.
4. Show the **threat detection panel** (if CrowdSec is configured).
5. Demonstrate the **runbook chat** — type a query and show RAG-grounded responses.

### Step 4: API Demo

Show the REST API directly:

```bash
# Health check (public)
curl http://localhost:8080/health

# Get current status (authenticated)
curl http://localhost:8080/status -b "session=<cookie>"

# Get recent alerts
curl http://localhost:8080/alerts -b "session=<cookie>"

# Switch agent mode
curl -X POST http://localhost:8080/api/agent/mode \
  -H "Content-Type: application/json" \
  -b "session=<cookie>" \
  -d '{"mode": "langchain"}'
```

### Step 5: Show the Code

Walk through key files in this order:
1. `agent/orchestrator.py` — the LangGraph state machine (collect/analyze/decide/notify)
2. `agent/llm/vertex.py` — LLM integration (structured JSON output)
3. `agent/rag/vector_store.py` — ChromaDB embeddings
4. `api/main.py` — FastAPI routes and middleware stack
5. `api/middleware/audit.py` — audit logging
6. `tests/test_agent.py` — test coverage demonstration

### Step 6: Run Tests

```bash
PYTHONPATH=. pytest -v --tb=short
```

Show that all tests pass and explain the mock-based testing strategy.

### Step 7: Show the Master's Project Report

The report is at `docs/masters_project/InfraGuard_Pro_Masters_Project.docx` (25,000+ words, 14 embedded figures). To rebuild it:

```bash
cd docs/masters_project
npm install docx
python figures/generate.py    # regenerate the 14 PNG figures
node build.js                  # build the .docx
```

---

## 6. Rebuilding the Master's Project Document

### 6.1 Prerequisites

```bash
cd docs/masters_project

# Install the docx library (once)
npm install -g docx

# Install matplotlib for figure generation (once)
pip install matplotlib numpy
```

### 6.2 Regenerate Figures

```bash
python figures/generate.py
```

This creates 14 PNG files in `figures/` at 220 DPI. Chapter 5 charts carry "Illustrative Projection" banners since the 150-finding evaluation has not been executed yet.

### 6.3 Build the Document

```bash
node build.js
```

Output: `InfraGuard_Pro_Masters_Project.docx` (~2.1 MB, 25,000+ words).

### 6.4 Post-Build Checklist

Before submission:
- [ ] Replace `[NAME OF STUDENT]` with your full name (cover page, certification)
- [ ] Replace `[Matriculation Number]` with your actual number
- [ ] Review page numbers in the Table of Contents against the rendered PDF
- [ ] Run through a plagiarism checker (Turnitin or equivalent)
- [ ] Verify all 45 references are accessible / resolvable
- [ ] Print a test copy to check formatting, margins, and figure placement

---

## 7. Production Deployment (GCE via GitHub Actions)

### 7.1 Terraform Setup

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your GCP project details

terraform init
terraform plan
terraform apply
```

This provisions: GCE VM, static IP, firewall rules, Artifact Registry, GCS backend.

### 7.2 GitHub Secrets

Set these secrets in your GitHub repository settings:
- `GCP_SA_KEY` — base64-encoded service account key
- `GCE_INSTANCE` — VM instance name
- `GCE_ZONE` — VM zone
- All `.env` variables as individual secrets

### 7.3 Deploy

Push to `main`. The GitHub Actions workflow (`.github/workflows/deploy.yml`) will:
1. Build Docker images for `api` and `agent`.
2. Push to Google Artifact Registry.
3. SSH into the VM and restart Docker Compose.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Model request is rejected | Provider key or model name is invalid | Check `LLM_PROVIDER` and its matching API key/model variables |
| DevPlanner aliases do not resolve | Shared Docker network is missing | Create `infraguard-observability` and recreate both Compose stacks |
| CrowdSec decision returns 401 | Machine credentials are missing or not registered | Register the machine in DevPlanner CrowdSec and copy the same credentials to both `.env` files |
| Dashboard returns 401 | Session cookie expired (24h max) | Log in again at `/login` |
| ChromaDB permission error | Volume not writable | Check `chroma_data` volume permissions |
| Tests fail with import errors | PYTHONPATH not set | Run with `PYTHONPATH=.` prefix |
| `docker compose` not found | Docker Compose v1 | Upgrade to Docker Compose v2 (`docker compose` without hyphen) |
| Agent crashes on Docker tool calls | Docker socket not mounted | Ensure `/var/run/docker.sock:/var/run/docker.sock:ro` in compose |
