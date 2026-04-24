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
provider = "Google Vertex AI"
model = "gemini-2.0-flash"
client = "google-cloud-aiplatform (vertexai)"
auth = "GOOGLE_APPLICATION_CREDENTIALS — service account JSON key path"
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

## Runtime notes

- **PYTHONPATH**: run commands from the `infraguard-ai/` directory (see `pytest.ini` and Docker `ENV PYTHONPATH=/app`).
- **SQLite path**: set `DB_PATH` to a shared path in Docker (compose uses `/data/verdicts.db`).
- **GCP credentials in Docker**: place your service account JSON at `secrets/infraguard-key.json` (gitignored). Compose mounts it to `/run/secrets/gcp-key.json`; set `GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/gcp-key.json` in `.env`.
- **Docker socket**: the agent mounts `/var/run/docker.sock` read-only for `docker_events`, `collect_container_diagnostics`, and `fetch_container_errors` (DevPlanner log tail from `main` heartbeat). Restrict the client to read-only API calls in code; `:ro` on the socket is not a full security boundary.
- **Docker builds**: `docker-compose.yml` uses `context: .` with `agent/Dockerfile` and `api/Dockerfile` (not separate image contexts, so `requirements.txt` stays at repo root).
- **Docker events**: uses `DOCKER_HOST` if set, otherwise the default unix socket when available inside the container.

## Cursor / assistant prompt (LLM section)

Use Google Vertex AI instead of AWS Bedrock. Install the `google-cloud-aiplatform` package. Use model `gemini-2.0-flash` (Vertex model ID; avoid legacy `-001` suffix unless your region publishes it). Authenticate with `GOOGLE_APPLICATION_CREDENTIALS` pointing to a service account JSON key. The `get_verdict()` function in `agent/llm/vertex.py` calls Vertex AI with `response_mime_type="application/json"` and returns a parsed dict with fields: `severity`, `summary`, `root_cause`, `recommended_action` (or `ok: False` plus error fields on failure).
