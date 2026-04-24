# InfraGuard AI — project context

This file is the single source of truth for assistants working on this repository. Keep it updated when behavior, endpoints, or configuration change.

```toml
[project]
name = "infraguard-ai"
description = "Agentic LLM platform for DevSecOps observability and automated threat response"
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
client = "google-genai (genai.Client, vertexai=True, API v1)"
auth = "GOOGLE_APPLICATION_CREDENTIALS — service account JSON key path (ADC)"
output_format = "JSON — severity, summary, root_cause, recommended_action"

[agent]
framework = "LangGraph"
schedule = "60 second asyncio heartbeat loop"
severity_levels = ["ok", "warning", "high", "critical"]
notify_on = ["high", "critical"]
docker_diagnostics_on = ["critical"]

[mcp_tools]
loki = "fetch_loki_logs() — last 50 lines"
prometheus = "query_prometheus() — CPU, RAM, disk, error rate"
docker_events = "get_docker_events() — restarts, unhealthy containers"
docker_api = "collect_container_diagnostics() — stats, logs, health via Docker socket"
docker_logs = "fetch_container_errors() — Docker SDK log tail + keyword filter (async); invoked from main heartbeat"
http_probe = "probe_endpoints() — status + latency"
notify = "send_push_notification() — ntfy.sh"

[api]
framework = "FastAPI"
storage = "SQLite via aiosqlite"
endpoints = ["/status", "/alerts", "/health"]
docker_port = "8080"

[dashboard]
type = "Single HTML page"
refresh_interval = "30 seconds"
served_by = "FastAPI static"

[notifications]
provider = "ntfy.sh"
topic = "NTFY_TOPIC env var"
priority_map = { ok = "min", warning = "default", high = "high", critical = "urgent" }

[env_vars]
required = ["LOKI_URL", "PROMETHEUS_URL", "DEVPLANNER_CONTAINER_NAME", "MONITORED_CONTAINERS", "GCP_PROJECT_ID", "GCP_REGION", "GOOGLE_APPLICATION_CREDENTIALS", "NTFY_TOPIC", "PROBE_URLS"]

[testing]
framework = "pytest + respx"
test_files = ["tests/test_tools.py", "tests/test_agent.py"]
```

## LLM Client

- **SDK**: `google-genai>=1.0.0` (replaces deprecated `google-cloud-aiplatform` / `vertexai` generative helpers for this app).
- **Model**: `gemini-2.5-flash` via Vertex AI Agent Platform (`agent/llm/vertex.py` uses `HttpOptions(api_version='v1')` and `vertexai=True`).
- **Auth**: GCP service account via `GOOGLE_APPLICATION_CREDENTIALS` (Application Default Credentials).
- **Config**: `GCP_PROJECT_ID`, `GCP_REGION` (default when unset: `us-central1`).
- **Note**: **Agent Platform APIs must be enabled on the GCP project.** If they are not, inference can fail with **404** responses that look like generic routing errors and are easy to misdiagnose. Enable and manage access in the [Google Cloud Agent Platform console](https://console.cloud.google.com/agent-platform).

## Runtime notes

- **PYTHONPATH**: run commands from the `infraguard-ai/` directory (see `pytest.ini` and Docker `ENV PYTHONPATH=/app`).
- **SQLite path**: set `DB_PATH` to a shared path in Docker (compose uses `/data/verdicts.db`).
- **GCP credentials in Docker**: place your service account JSON at `secrets/infraguard-key.json` (gitignored). Compose mounts it to `/run/secrets/gcp-key.json`; set `GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/gcp-key.json` in `.env`.
- **Docker socket**: the agent mounts `/var/run/docker.sock` read-only for `docker_events`, `collect_container_diagnostics`, and `fetch_container_errors` (DevPlanner log tail from `main` heartbeat). Restrict the client to read-only API calls in code; `:ro` on the socket is not a full security boundary.
- **Docker builds**: `docker-compose.yml` uses `context: .` with `agent/Dockerfile` and `api/Dockerfile` (not separate image contexts, so `requirements.txt` stays at repo root).
- **Docker events**: uses `DOCKER_HOST` if set, otherwise the default unix socket when available inside the container.

## Cursor / assistant prompt (LLM section)

Use **Google Vertex AI** via the **`google-genai`** SDK (not AWS Bedrock). Install `google-genai>=1.0.0`. Use model **`gemini-2.5-flash`** with `genai.Client(..., vertexai=True, http_options=HttpOptions(api_version='v1'))`. Authenticate with **`GOOGLE_APPLICATION_CREDENTIALS`** pointing to a service account JSON key. The `get_verdict()` function in `agent/llm/vertex.py` calls `client.models.generate_content` with `response_mime_type="application/json"` and returns a parsed dict with fields: `severity`, `summary`, `root_cause`, `recommended_action` (or `ok: False` plus error fields on failure). Ensure **Agent Platform APIs are enabled** on the project (see **LLM Client** above) or expect misleading **404s**.
