# InfraGuard AI

**InfraGuard AI** is a self-hosted, LLM-assisted DevSecOps observability reference implementation. It collects selected telemetry from web applications, containers, and VMs and produces advisory health and incident-triage verdicts for operator review. It is designed for supervised triage and controlled evaluation; it is not an autonomous SRE or a production-validated incident-response system.

---

## Basic Explanation & App Flow

<img width="425" height="306" alt="image" src="https://github.com/user-attachments/assets/354f2357-90d9-472b-b63f-b8decd700ee3" />


How does InfraGuard AI work?

1. **Telemetry Collection**: Every 120 seconds (configurable via `HEARTBEAT_INTERVAL_SECONDS`), the InfraGuard **Agent** wakes up and gathers data from your infrastructure:
   - **Loki**: Fetches the most recent log lines from an explicit time window (`query_range`, newest first).
   - **Prometheus**: Checks CPU, memory, disk, and HTTP error rate metrics.
   - **HTTP Probes**: Pings your endpoints to ensure they are online and responsive.
   - **Docker** *(optional, off by default)*: With `ENABLE_DOCKER_MONITORING=1`, scans container events (crashes, restarts, unhealthy transitions), tails the target container's error logs each heartbeat, and gathers per-container diagnostics when a verdict is high/critical. Requires the Docker socket mount in `docker-compose.yml`.
2. **AI Reasoning**: The agent sends this telemetry to a direct frontier-model API. Gemini is the default, Anthropic is a first-class alternative, and OpenAI or local Ollama remain available. With `USE_LANGCHAIN_AGENT=1`, a LangChain multi-tool agent queries Loki, Prometheus, and HTTP probes itself; otherwise the app makes one structured model call over the collected telemetry.
3. **Verdict Generation**: The AI returns a strict JSON verdict — `severity` (`ok`, `warning`, `high`, `critical`), `summary`, `root_cause`, and `recommended_action`. Verdicts are saved to SQLite and pruned automatically after `VERDICT_RETENTION_DAYS` (default 30).
4. **Notifications**: `high` and `critical` verdicts trigger a push notification via [ntfy.sh](https://ntfy.sh) (`NTFY_TOPIC`).
5. **Dashboard**: The secure **InfraGuard Dashboard** (served by the API on port **8080**) shows the current verdict, integration status chips, a check history, threat detection, and a runbook chat assistant. If the agent stops reporting, a stale-data banner appears.
6. **Threat Detection & Response**: The API scans recent Loki logs (up to 500 lines) for HTTP brute force, SSH brute force, and port-scan patterns. Each detected threat gets a **Block IP** button — one click builds a CrowdSec ban decision server-side and applies it via the CrowdSec Local API. Without CrowdSec configured, the action runs in **dry-run** mode (logged, not applied).
7. **Runbook Context (RAG)**: Markdown runbooks under `./runbooks` are embedded locally, indexed in **ChromaDB**, and queried from the dashboard chat. Use the **⟳ Re-index** button after adding or changing a runbook.

---

## Tools & Technologies Used

- **Backend Framework**: Python (FastAPI for the dashboard/API, asyncio heartbeat loop for the Agent).
- **AI / LLM**: Direct Gemini Developer API by default, with Anthropic, OpenAI, and local Ollama provider options; LangChain and LangGraph handle agentic reasoning.
- **RAG (Retrieval-Augmented Generation)**: ChromaDB with local ONNX embeddings and Markdown runbooks.
- **Observability Stack**: Prometheus (metrics), Grafana Loki (logs), Promtail (log shipping).
- **Security**: CrowdSec (operator-approved IP bans), signed session cookies, enforced rate limiting (60 req/min per IP, 5/min on login), security headers + CSP, audit logging of every request, HTML-escaped rendering of all LLM/log-derived text.
- **Deployment**: Docker Compose, GitHub Actions (CI/CD), Terraform, Google Compute Engine (GCE).

---

## Environment Variables

Configure these in your `.env` file (see `.env.example` for a complete annotated template). **Keep comments on their own lines** — Docker Compose's `env_file` does not strip inline comments.

### 1. Core Security & Authentication
- `INFRAGUARD_USERNAME` / `INFRAGUARD_PASSWORD` — Dashboard credentials.
- `SECRET_KEY` — Random cryptographic string for signing session cookies.
- `SESSION_COOKIE_SECURE` — Set to `1` once the dashboard is served over HTTPS.

### 2. Model APIs
- `LLM_PROVIDER` — `gemini` (default), `anthropic`, `openai`, or `ollama`.
- `GEMINI_API_KEY` / `GEMINI_MODEL` — Direct Gemini Developer API credentials and model selection.
- `ANTHROPIC_API_KEY` / `ANTHROPIC_MODEL` — Claude API credentials and model selection.
- `OPENAI_API_KEY` / `OPENAI_MODEL` — OpenAI API credentials and model selection.
- `USE_LANGCHAIN_AGENT` — `1` enables multi-tool AI reasoning (recommended).

### 3. Observability Endpoints
- `LOKI_URL` — Loki instance URL (also powers the threat scanner).
- `PROMETHEUS_URL` — Prometheus instance URL.
- `PROBE_URLS` — Comma-separated URLs to ping for uptime checks.

### 4. Docker Monitoring (optional)
- `ENABLE_DOCKER_MONITORING` — `1` to scan container events and gather diagnostics (off by default).
- `MONITORED_CONTAINERS` — Comma-separated container names to inspect on high/critical verdicts.
- `DEVPLANNER_CONTAINER_NAME` — Container whose error log lines are tailed each heartbeat.
- `DOCKER_HOST` — Docker Engine endpoint (leave empty for the default unix socket).

### 5. Notifications & Storage
- `NTFY_TOPIC` — ntfy.sh topic for high/critical push alerts.
- `DB_PATH` — SQLite path (compose uses `/data/verdicts.db`).
- `VERDICT_RETENTION_DAYS` — Auto-prune verdicts older than this (default 30).
- `HEARTBEAT_INTERVAL_SECONDS` — Agent check interval (default 120).

### 6. Runbooks
- `RUNBOOKS_DIR` — Directory containing local Markdown runbooks; Compose uses `/app/runbooks`.

### 7. Threat Response (optional)
- `CROWDSEC_API_URL` / `CROWDSEC_API_KEY` — CrowdSec Local API for applying IP bans. Without these, bans run in dry-run mode.

---

## Setup & Deployment

> [!WARNING]
> **The included Terraform, Docker Compose, and GitHub Actions files are a safer demonstration baseline, not a complete production security implementation.** Before operational use, terminate and enforce HTTPS at a reviewed ingress or reverse proxy; expose only port 443 to approved source ranges; keep the dashboard/API (8080), Loki (3100), and Prometheus (9090) on loopback or trusted private/VPN networks; set `SESSION_COOKIE_SECURE=1`; place credentials and API keys in a managed secret store rather than a repository or long-lived plaintext `.env` file; grant service identities only the permissions they require; and independently verify firewall rules, TLS configuration, secret delivery, authentication, backup/recovery, monitoring, and incident-response controls. Port 80 must remain disabled unless it performs an immediate redirect to HTTPS. The repository does **not** provision a TLS certificate, reverse proxy, or managed secret integration for you.

### Local Demo / Development
For a same-server demonstration, no public ingress, VPN, or TLS endpoint is required: run the browser on the server and use the loopback-bound dashboard.

1. Copy the example env file: `cp .env.example .env`.
2. Set `GEMINI_API_KEY` for the default provider, or switch `LLM_PROVIDER` and add the matching provider key.
3. Start the app: `docker compose up -d --build api agent`.
4. On that server, open **`http://127.0.0.1:8080`** and log in.

The Compose file does not start Loki or Prometheus. For a same-server demo, set `LOKI_URL` and `PROMETHEUS_URL` only when those services are reachable by hostname from the app containers—for example, after attaching them to a shared Docker network. `localhost` and `127.0.0.1` inside a container refer to that container, not the server. Leave either variable blank to skip that optional collector. Notifications are also disabled until `NTFY_TOPIC` is explicitly configured.

### Production Deployment (GitHub Actions → GCE)
The `.github/workflows/deploy.yml` pipeline runs on every push to `main`. It assumes a separately configured HTTPS reverse proxy or load balancer on the VM because Docker Compose binds the dashboard/API to `127.0.0.1:8080`:
1. Runs the test suite (`pytest`).
2. Builds the `agent` and `api` images and pushes them to Google Artifact Registry.
3. SSHs into your VM, regenerates a mode-`0600` `.env` from GitHub Secrets (including `NTFY_TOPIC` and `PROBE_URLS`), enables secure cookies, and restarts Docker Compose.

This workflow still materialises secrets in a VM-local `.env` file and therefore does not meet the managed-secret requirement on its own. For production, replace that step with a managed secret service and short-lived workload identity, then verify secret rotation and least-privilege access. Do not make port 8080 public to compensate for a missing HTTPS proxy.

Pull requests run tests via `.github/workflows/test.yml`.

### Indexing Local Runbooks
Add, change, or remove Markdown files under `./runbooks`, then click **⟳ Re-index** on the dashboard's Runbook Assistant card or call the endpoint directly. Re-indexing uses stable document identities: changed files are updated, deleted files are removed, and repeated refreshes do not create duplicates. A failed refresh returns an error instead of reporting a false success.
```bash
curl -X POST http://localhost:8080/api/runbooks/index -b "session=<your_session_cookie>"
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Dashboard (requires session) |
| GET/POST | `/login`, GET `/logout` | Session auth (login limited to 5 attempts/min) |
| GET | `/health` | Liveness check (public) |
| GET | `/status` | Latest verdict + staleness info (`age_seconds`, `stale`) |
| GET | `/alerts` | Recent check history (last 20 verdicts) |
| GET | `/api/config` | Which integrations are configured (booleans only) |
| GET | `/api/agent/mode` | Active reasoning mode + model |
| POST | `/api/verdicts/ack` | Mark an existing `ok`/`warning` condition as known for 1–365 days |
| POST | `/api/verdicts/unack` | Remove an acknowledgement |
| GET | `/api/acks` | List active acknowledgements |
| GET | `/api/threats` | Scan recent Loki logs for attack patterns |
| POST | `/api/threats/apply` | Apply a CrowdSec ban for a detected threat (dry-run without CrowdSec) |
| POST | `/api/runbooks/query` | Ask the runbook RAG assistant a question |
| POST | `/api/runbooks/index` | Synchronise local Markdown runbooks with ChromaDB |

All routes except `/health` and `/login` require an authenticated session.
