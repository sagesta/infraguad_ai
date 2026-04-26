# InfraGuard AI

**InfraGuard AI** is an agentic DevSecOps observability platform. It monitors your applications (such as DevPlanner), analyzes telemetry (logs, metrics, and HTTP probes) using Google Vertex AI (Gemini 2.5 Flash), and automatically detects threats or infrastructure failures.

## Key Features

1. **Agentic Observability (Gemini 2.5 Flash)**
   - Integrates with Loki, Prometheus, and Docker events.
   - Evaluates system health and provides root cause analysis and recommended actions.
   - Operates in either single-shot mode or using **LangChain** multi-tool reasoning (`USE_LANGCHAIN_AGENT=1`).

2. **Automated Threat Detection**
   - Scans Loki logs for SSH brute forcing, HTTP brute forcing, and port scans.
   - Proposes actionable CrowdSec decisions to ban malicious IPs (supports dry-run mode when CrowdSec is not installed).

3. **RAG Runbook Assistant**
   - Connects to Notion to index runbooks into a local ChromaDB vector store.
   - Provides a conversational AI interface on the dashboard to query runbooks during incidents.

4. **Secure Dashboard & API**
   - Modern dark-mode UI with severity badges, threat panels, and a runbook chat interface.
   - **Authentication**: Session-cookie based login system (`INFRAGUARD_USERNAME`, `INFRAGUARD_PASSWORD`).
   - **Security Hardening**: Strict CSP/security headers, rate limiting (60/min), and audit logging (`audit.log`).

5. **Cloud-Native Infrastructure**
   - **Terraform** configuration for deploying to Google Cloud Engine (GCE) with Artifact Registry.
   - **GitHub Actions** CI/CD pipeline for automated testing and deployment.
   - **Promtail** configuration for pushing local VM logs to a cloud Loki instance.

## Setup Instructions

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in the required values:

```bash
cp .env.example .env
```

**Note:** Set `USE_LANGCHAIN_AGENT=1` in your `.env` to enable full LangChain agentic reasoning (recommended for demo).

**Required Secrets:**
- `INFRAGUARD_USERNAME` / `INFRAGUARD_PASSWORD` — Dashboard login credentials.
- `SECRET_KEY` — Random string for session cookie signing.
- `GCP_PROJECT_ID` — Your Google Cloud project ID.
- `GOOGLE_APPLICATION_CREDENTIALS` — Path to your GCP Service Account JSON key (must have Vertex AI access).
- `NOTION_TOKEN` / `NOTION_DATABASE_ID` — Required for the RAG runbook assistant.

### 2. Local Development

Run the entire stack locally using Docker Compose:

```bash
docker compose up -d --build
```

The dashboard will be available at `http://localhost:8080`. You will be redirected to `/login`.

### 3. Loading Notion Runbooks

To index your runbooks from Notion into ChromaDB:

```bash
curl -X GET http://localhost:8080/api/runbooks/index -b "session=<your_session_cookie>"
```
*(Or navigate to `/api/runbooks/index` in an authenticated browser window).*

### 4. Promtail Setup (Log Shipping)

To push logs from a standalone VM to your cloud Loki instance:

```bash
cd promtail
sudo bash setup.sh <YOUR_LOKI_URL>
```
This will download Promtail, configure it to scrape system logs and Docker logs, and start it as a systemd service.

## Architecture

- **Agent Component (`agent/`)**: Runs a 60-second LangGraph loop. Collects Docker events, queries telemetry, and invokes Gemini via Vertex AI to generate verdicts.
- **API Component (`api/`)**: Serves the dashboard, handles authentication, and exposes endpoints for threats and RAG queries.
- **Data Stores**: Uses `aiosqlite` for verdict persistence and ChromaDB for vector embeddings.

For deeper technical details, see [CONTEXT.md](./CONTEXT.md).
