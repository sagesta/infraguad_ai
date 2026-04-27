# InfraGuard AI

**InfraGuard AI** is an intelligent, self-hosted DevSecOps observability agent. It continuously monitors your infrastructure (like web apps, containers, and VMs) and acts as an automated Site Reliability Engineer (SRE). Instead of just showing you dashboards, InfraGuard uses AI to read logs, analyze metrics, and automatically determine if your system is healthy, under attack, or failing.

---

## Basic Explanation & App Flow

How does InfraGuard AI work?

1. **Telemetry Collection**: Every 120 seconds, the InfraGuard **Agent** wakes up and gathers data from your infrastructure:
   - **Loki**: Fetches recent application and system error logs.
   - **Prometheus**: Checks CPU, memory, disk, and HTTP error rate metrics.
   - **Docker**: Scans for containers that have crashed, restarted, or become unhealthy.
   - **HTTP Probes**: Pings your endpoints to ensure they are online and responsive.
2. **AI Reasoning (Vertex AI)**: The agent sends this raw data to **Google Vertex AI** (using the Gemini 2.5 Flash model). The AI acts as an SRE, reasoning through the data using LangChain tools to diagnose root causes and recommend actions.
3. **Runbook Context**: Before deciding on an action, the agent fetches relevant IT Runbooks directly from a **Notion Database**. This ensures the AI's recommendations match your company's actual procedures.
4. **Verdict Generation**: The AI generates a final JSON verdict (e.g., `ok`, `warning`, `high`, `critical`) alongside a plain-English summary, root cause analysis, and recommended action.
5. **Dashboard & Threat Response**: The verdict is saved to a local SQLite database and displayed on the secure **InfraGuard Dashboard** (served by the API). The system also scans for active attacks (like SSH brute forcing) and can auto-generate firewall rules using CrowdSec.

---

## Tools & Technologies Used

- **Backend Framework**: Python (FastAPI for the dashboard/API, standard Python for the Agent loop).
- **AI / LLM**: Google Vertex AI (Gemini 2.5 Flash) via LangChain and LangGraph for agentic reasoning.
- **RAG (Retrieval-Augmented Generation)**: ChromaDB (Vector Store) and Notion API for fetching and querying runbooks.
- **Observability Stack**: Prometheus (Metrics), Grafana Loki (Logs), Promtail (Log Shipping).
- **Security**: CrowdSec (IP banning), secure session cookies, strict CORS/CSP policies.
- **Deployment**: Docker Compose, GitHub Actions (CI/CD), Terraform, Google Compute Engine (GCE).

---

## Environment Variables Needed

To run InfraGuard AI, you must configure the following variables in your `.env` file (see `.env.example`):

### 1. Core Security & Authentication
- `INFRAGUARD_USERNAME` — Your desired username for the dashboard.
- `INFRAGUARD_PASSWORD` — Your desired password for the dashboard.
- `SECRET_KEY` — A random cryptographic string for signing session cookies.

### 2. Google Cloud / AI Authentication
- `GCP_PROJECT_ID` — Your Google Cloud Project ID.
- `GCP_REGION` — Your Google Cloud Region (e.g., `us-central1`).
- `GOOGLE_APPLICATION_CREDENTIALS` — Absolute path to your GCP Service Account JSON key (must have Vertex AI user permissions).
- `USE_LANGCHAIN_AGENT` — Set to `1` to enable full multi-tool AI reasoning (recommended).

### 3. Observability Endpoints
- `LOKI_URL` — The URL to your Loki instance (e.g., `http://100.66.123.4:3100`).
- `PROMETHEUS_URL` — The URL to your Prometheus instance (e.g., `http://100.66.123.4:9090`).
- `PROBE_URLS` — Comma-separated URLs to ping for uptime checking (e.g., `https://my-app.com/health`).

### 4. Runbooks (Notion RAG)
- `NOTION_TOKEN` — Your Notion Internal Integration Token.
- `NOTION_DATABASE_ID` — The ID of the Notion Database containing your runbooks.

### 5. Security (Optional)
- `CROWDSEC_API_URL` / `CROWDSEC_API_KEY` — (Optional) To push automated IP bans to your CrowdSec Local API.

---

## Setup & Deployment

### Local Development
1. Copy the example env file: `cp .env.example .env`
2. Fill out the variables listed above.
3. Start the stack: `docker compose up -d --build`
4. Access the dashboard at `http://localhost:8000` (Login required).

### Production Deployment (GitHub Actions to GCE)
The project includes a `.github/workflows/deploy.yml` pipeline. When you push to `main`:
1. It builds the Docker images for the `agent` and `api`.
2. It pushes them to Google Artifact Registry.
3. It SSHs into your VM, updates the `.env` file using GitHub Secrets, and restarts Docker Compose.

### Indexing Notion Runbooks
Once the app is running, index your runbooks from Notion into the AI's memory by triggering the endpoint:
```bash
curl -X GET http://localhost:8000/api/runbooks/index -b "session=<your_session_cookie>"
```
*(Or simply navigate to `/api/runbooks/index` in an authenticated browser).*
