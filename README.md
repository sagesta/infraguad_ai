# InfraGuard AI

InfraGuard AI is an AI-powered SRE assistant for small cloud/container environments. It watches logs and metrics, classifies incidents (`OK`, `WARNING`, `CRITICAL`), explains root cause in plain English, and recommends next actions for operators.

## What This Project Uses

### Core Services
- **API + Dashboard (`api/`)**: FastAPI service that provides auth, status APIs, threat APIs, and the web dashboard UI.
- **Agent (`agent/`)**: Background loop that fetches telemetry, calls Vertex AI, and writes verdicts.
- **Storage**:
  - `aiosqlite` for verdict history.
  - ChromaDB for runbook embeddings (RAG).

### External Integrations
- **Prometheus**: Metrics source (availability, health, rates, system behavior).
- **Loki**: Log source (application/system events).
- **Google Vertex AI (Gemini)**: LLM analysis engine used by the agent.
- **Notion**: Source of incident runbooks for the Runbook Assistant.
- **CrowdSec (optional)**: Suggested response actions for detected threats.

### Platform / Delivery
- **Docker + Docker Compose** for runtime.
- **GitHub Actions** for CI/CD.
- **Google Artifact Registry** for image hosting.
- **GCE VM** for deployment target.
- **Terraform (`terraform/`)** for infrastructure provisioning.

## End-to-End Flow (How InfraGuard Works)

1. **Telemetry collection**
   - Prometheus and Loki expose current metrics/logs.
   - The agent also inspects Docker/container context when needed.

2. **AI analysis**
   - The agent packages recent telemetry into an LLM prompt.
   - Vertex AI returns structured analysis (severity, summary, root cause, actions).

3. **Persistence**
   - Verdicts are saved to SQLite so the API/dashboard can serve current and historical state.

4. **Operator view**
   - Dashboard shows current status, alerts, and threat panel.
   - API endpoints expose the same data for integrations/automation.

5. **Runbook guidance (RAG layer)**
   - Runbooks can be indexed from Notion into ChromaDB.
   - The assistant answers incident questions grounded in your runbook content.

## Service/API Flow At Runtime

`Loki + Prometheus -> Agent (LLM analysis) -> SQLite verdicts -> API -> Dashboard`

Key endpoints:
- `GET /health` -> API health (`{"status":"ok"}`)
- `GET /status` -> current incident status payload
- `GET /dashboard` -> green-ready summary payload
- `GET /alerts` -> recent incident history
- `GET /api/threats` -> threat analysis output
- `GET /api/runbooks/index` -> trigger runbook indexing from Notion
- `POST /api/runbooks/query` -> ask runbook assistant

## Quick Start (Local)

1. Copy environment template:
```bash
cp .env.example .env
```

2. Set required env values in `.env`:
- `INFRAGUARD_USERNAME`, `INFRAGUARD_PASSWORD`, `SECRET_KEY`
- `GCP_PROJECT_ID`, `GCP_REGION`, `GOOGLE_APPLICATION_CREDENTIALS`
- `LOKI_URL`, `PROMETHEUS_URL`
- `NOTION_TOKEN`, `NOTION_DATABASE_ID` (for runbooks)

3. Start stack:
```bash
docker compose up -d --build
```

4. Open dashboard:
- `http://localhost:8000/login`

## Deployment Flow (Main Branch)

On push to `main`, workflow in `.github/workflows/deploy.yml`:
1. Runs tests.
2. Builds/pushes `agent` and `api` images to Artifact Registry.
3. Connects to GCE VM.
4. Writes runtime `.env` from GitHub Secrets on VM.
5. Pulls latest images and restarts `docker compose`.
6. Validates deployment via `curl /health`.

## Project Structure

- `agent/` - telemetry collectors, LLM orchestration, threat logic
- `api/` - FastAPI app, auth/session middleware, endpoints
- `dashboard/` - web UI assets
- `terraform/` - cloud infrastructure definitions
- `promtail/` - optional log shipping setup

For deeper implementation notes, see `CONTEXT.md`.
