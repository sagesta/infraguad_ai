# InfraGuard AI — project context

This file is the single source of truth for assistants working on this repository. Keep it updated when behavior, endpoints, or configuration change.

```toml
[project]
name = "infraguard-ai"
description = "Agentic LLM platform for DevSecOps observability, automated threat response, and RAG runbooks"
language = "Python 3.11+"
package_manager = "pip + requirements.txt"
containerized = true
compose_file = "docker-compose.yml"

[target]
app = "DevPlanner (Hono + PostgreSQL + Redis)"
connectivity = "Same host as InfraGuard; Docker Compose internal DNS (service names)"
metrics_url = "PROMETHEUS_URL env var"
logs_url = "LOKI_URL env var"
docker_monitored = "MONITORED_CONTAINERS env var (comma-separated container names)"
devplanner_logs_container = "DEVPLANNER_CONTAINER_NAME — Docker container name for log error tail (main heartbeat)"

[llm]
provider = "Google Vertex AI (Agent Platform)"
model = "gemini-2.5-flash"
client = "google-genai (genai.Client, vertexai=True, API v1) or langchain-google-vertexai (ChatVertexAI)"
auth = "GOOGLE_APPLICATION_CREDENTIALS — service account JSON key path (ADC)"
output_format = "JSON — severity, summary, root_cause, recommended_action"

[agent]
framework = "LangGraph + LangChain"
schedule = "60 second asyncio heartbeat loop"
severity_levels = ["ok", "warning", "high", "critical"]
notify_on = ["high", "critical"]
docker_diagnostics_on = ["critical"]
langchain_mode = "USE_LANGCHAIN_AGENT=1 uses LangChain multi-tool reasoning instead of single-shot Gemini"

[mcp_tools]
loki = "fetch_loki_logs() — last 50 lines"
prometheus = "query_prometheus() — CPU, RAM, disk, error rate"
docker_events = "get_docker_events() — restarts, unhealthy containers"
docker_api = "collect_container_diagnostics() — stats, logs, health via Docker socket"
docker_logs = "fetch_container_errors() — Docker SDK log tail + keyword filter (async); invoked from main heartbeat"
http_probe = "probe_endpoints() — status + latency"
notify = "send_push_notification() — ntfy.sh"
threats = "analyze_threats() / apply_crowdsec_decision() — CrowdSec integration"

[api]
framework = "FastAPI"
storage = "SQLite via aiosqlite"
endpoints = ["/status", "/alerts", "/health", "/login", "/logout", "/api/threats", "/api/threats/apply", "/api/runbooks/query", "/api/runbooks/index"]
docker_port = "8080"
middleware = ["SecurityHeadersMiddleware", "AuditMiddleware", "AuthMiddleware"]
auth = "Cookie-based session using itsdangerous, INFRAGUARD_USERNAME and INFRAGUARD_PASSWORD env vars"

[rag]
vector_store = "ChromaDB (local to chroma_data volume)"
embeddings = "VertexAI text-embedding-004"
loader = "Notion API via notion-client"

[dashboard]
type = "Single HTML page (dark mode)"
refresh_interval = "30 seconds"
served_by = "FastAPI static"
features = ["Severity cards", "Alerts table", "Threat detection panel", "Runbook chat UI"]

[notifications]
provider = "ntfy.sh"
topic = "NTFY_TOPIC env var"
priority_map = { ok = "min", warning = "default", high = "high", critical = "urgent" }

[env_vars]
required = ["LOKI_URL", "PROMETHEUS_URL", "DEVPLANNER_CONTAINER_NAME", "MONITORED_CONTAINERS", "GCP_PROJECT_ID", "GCP_REGION", "GOOGLE_APPLICATION_CREDENTIALS", "NTFY_TOPIC", "PROBE_URLS", "SECRET_KEY", "INFRAGUARD_USERNAME", "INFRAGUARD_PASSWORD"]

[testing]
framework = "pytest + respx"
test_files = ["tests/test_tools.py", "tests/test_agent.py"]

[infrastructure]
terraform = "Google Cloud resources (GCE VM, IP, Firewall, Artifact Registry, GCS backend)"
ci_cd = "GitHub Actions (.github/workflows/deploy.yml)"
log_collection = "Promtail pushing local logs to cloud Loki (promtail/config.yml)"
```

## LLM Client

- **SDK**: `google-genai>=1.0.0` for basic access, `langchain-google-vertexai` for advanced reasoning.
- **Model**: `gemini-2.5-flash` via Vertex AI Agent Platform.
- **Auth**: GCP service account via `GOOGLE_APPLICATION_CREDENTIALS` (Application Default Credentials).
- **Config**: `GCP_PROJECT_ID`, `GCP_REGION` (default when unset: `us-central1`).
- **Note**: **Agent Platform APIs must be enabled on the GCP project.** If they are not, inference can fail with **404** responses that look like generic routing errors and are easy to misdiagnose. Enable and manage access in the [Google Cloud Agent Platform console](https://console.cloud.google.com/agent-platform).

## Runtime notes

- **PYTHONPATH**: run commands from the `infraguard-ai/` directory (see `pytest.ini` and Docker `ENV PYTHONPATH=/app`).
- **SQLite path**: set `DB_PATH` to a shared path in Docker (compose uses `/data/verdicts.db`).
- **GCP credentials in Docker**: place your service account JSON **file** at `secrets/gcp-key.json` (gitignored). Compose mounts it to `/run/secrets/gcp-key.json`; set `GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/gcp-key.json` in `.env`. If the host path is a directory by mistake, the container sees a directory at the mount target and ADC fails in non-obvious ways—remove the wrong path and use a single JSON file only.
- **Docker socket**: the agent mounts `/var/run/docker.sock` read-only for `docker_events`, `collect_container_diagnostics`, and `fetch_container_errors` (DevPlanner log tail from `main` heartbeat). Restrict the client to read-only API calls in code; `:ro` on the socket is not a full security boundary.
- **Docker builds**: `docker-compose.yml` uses `context: .` with `agent/Dockerfile` and `api/Dockerfile` (not separate image contexts, so `requirements.txt` stays at repo root).
- **Docker events**: uses `DOCKER_HOST` if set, otherwise the default unix socket when available inside the container.
- **Auth**: Only `/health` and `/login` are public. All other API and dashboard routes require an active session cookie.

## Cursor / assistant prompt (LLM section)

Use **Google Vertex AI** via the **`google-genai`** SDK or **LangChain** wrappers. Install `google-genai>=1.0.0` and `langchain-google-vertexai`. Use model **`gemini-2.5-flash`**. Authenticate with **`GOOGLE_APPLICATION_CREDENTIALS`** pointing to a service account JSON key. For multi-tool reasoning, the agent can use `agent/llm/langchain_agent.py` by setting `USE_LANGCHAIN_AGENT=1`. Ensure **Agent Platform APIs are enabled** on the project (see **LLM Client** above) or expect misleading **404s**.
