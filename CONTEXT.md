# InfraGuard AI — project context

This file is the single source of truth for assistants working on this repository. Keep it updated when behavior, endpoints, or configuration change.

```toml
[project]
name = "infraguard-ai"
description = "Agentic LLM platform for DevSecOps observability, operator-approved threat response, and RAG runbooks"
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
provider = "Configurable direct API: Gemini (default), Anthropic, OpenAI, or local Ollama"
model = "gemini-3.6-flash by default; provider-specific env override"
client = "google-genai or langchain-google-genai for Gemini; provider-native clients for alternatives"
auth = "GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY; Ollama needs no key"
output_format = "JSON — severity, summary, root_cause, recommended_action"

[agent]
framework = "LangGraph + LangChain"
schedule = "asyncio heartbeat loop, HEARTBEAT_INTERVAL_SECONDS (default 120)"
severity_levels = ["ok", "warning", "high", "critical"]
notify_on = ["high", "critical"]
docker_monitoring = "Opt-in via ENABLE_DOCKER_MONITORING=1 (off by default; needs Docker socket mount)"
docker_diagnostics_on = ["high", "critical"]
langchain_mode = "USE_LANGCHAIN_AGENT=1 uses LangChain multi-tool reasoning instead of a direct single call"
llm_mode_field = "Each verdict includes llm_mode ('langchain' or 'direct') to track which reasoning path produced it"

[agent_tools]
loki = "fetch_loki_logs(limit=50, window_minutes=15) — query_range, newest-first, explicit time window"
prometheus = "query_prometheus() — CPU, RAM, disk, error rate"
docker_events = "get_docker_events() — restarts, unhealthy containers (only when ENABLE_DOCKER_MONITORING=1)"
docker_api = "collect_container_diagnostics() — slim status/health/stats/log-tail summary on high/critical verdicts"
docker_logs = "fetch_container_errors() — Docker SDK log tail + keyword filter (async); invoked from main heartbeat when enabled"
http_probe = "probe_endpoints() — status + latency"
notify = "send_push_notification() — ntfy.sh"
threats = "analyze_threats() / suggest_crowdsec_decision() / apply_crowdsec_decision() — CrowdSec integration"

[api]
framework = "FastAPI"
storage = "SQLite via aiosqlite; verdicts pruned after VERDICT_RETENTION_DAYS (default 30)"
endpoints = ["/", "/status", "/alerts", "/health", "/login", "/logout", "/api/config", "/api/agent/mode", "/api/threats", "POST /api/threats/apply", "POST /api/runbooks/query", "POST /api/runbooks/index"]
docker_port = "8080"
middleware_order = "Audit (outermost) -> SecurityHeaders -> SlowAPI rate limit -> Auth (innermost); registered in reverse because Starlette wraps last-added outermost"
rate_limits = "60/minute per IP default; 5/minute on POST /login"
auth = "Cookie-based session using itsdangerous, INFRAGUARD_USERNAME and INFRAGUARD_PASSWORD env vars; SESSION_COOKIE_SECURE=1 marks the cookie Secure for HTTPS"
blocking_work = "Sync LLM/Loki calls inside async routes are wrapped in asyncio.to_thread to keep the event loop responsive"

[threat_response]
detection = "GET /api/threats fetches up to 500 recent Loki lines and scans for HTTP brute force (>=10 401/403s per IP), SSH brute force (>=10 auth failures), port scans (>=20 connection attempts)"
response = "Dashboard 'Block IP' button -> POST /api/threats/apply with the threat object; the CrowdSec decision is built server-side (suggest_crowdsec_decision) and applied via the Local API. Dry-run when CROWDSEC_API_URL is unset."

[rag]
vector_store = "ChromaDB (local to chroma_data volume)"
embeddings = "Local ONNX all-MiniLM-L6-v2 embeddings"
loader = "Markdown files under RUNBOOKS_DIR"
reindex = "POST /api/runbooks/index, triggered by the dashboard '⟳ Re-index' button"

[dashboard]
type = "Single HTML page (dark mode)"
refresh_interval = "30 seconds (status/history), 60 seconds (threats)"
served_by = "FastAPI static"
features = ["Integration status chips (/api/config)", "Stale-agent banner", "Severity verdict card", "Check History table with issues-only filter", "Threat panel with Block IP buttons", "Runbook chat UI with Re-index button"]
xss = "All server/LLM/log-derived text is HTML-escaped via esc() before innerHTML"

[notifications]
provider = "ntfy.sh"
topic = "NTFY_TOPIC env var"
priority_map = { ok = "min", warning = "default", high = "high", critical = "urgent" }

[env_vars]
required = ["SECRET_KEY", "INFRAGUARD_USERNAME", "INFRAGUARD_PASSWORD", "one provider key unless LLM_PROVIDER=ollama"]
optional = ["LLM_PROVIDER", "GEMINI_MODEL", "ANTHROPIC_MODEL", "OPENAI_MODEL", "LOKI_URL", "PROMETHEUS_URL", "PROBE_URLS", "NTFY_TOPIC", "CROWDSEC_API_URL", "CROWDSEC_API_KEY", "USE_LANGCHAIN_AGENT", "ENABLE_DOCKER_MONITORING", "MONITORED_CONTAINERS", "DEVPLANNER_CONTAINER_NAME", "DOCKER_HOST", "HEARTBEAT_INTERVAL_SECONDS", "VERDICT_RETENTION_DAYS", "SESSION_COOKIE_SECURE", "REGISTRY", "DB_PATH", "RUNBOOKS_DIR"]

[testing]
framework = "pytest + respx (asyncio_mode=auto)"
test_files = ["tests/test_tools.py", "tests/test_agent.py", "tests/test_api.py", "tests/test_store.py", "tests/test_rag.py", "tests/test_threat_response.py"]

[infrastructure]
terraform = "Google Cloud resources (GCE VM, IP, Firewall, Artifact Registry, GCS backend)"
ci_cd = "GitHub Actions: test.yml on PRs; deploy.yml on main (tests -> build/push images -> SSH deploy with regenerated .env)"
log_collection = "Promtail pushing local logs to cloud Loki (promtail/config.yml)"
```

## LLM Clients

- **Default**: Gemini Developer API through `google-genai` and `langchain-google-genai`, using `GEMINI_API_KEY` and `GEMINI_MODEL`.
- **Anthropic**: Claude API through `anthropic` and `langchain-anthropic`, using `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL`.
- **Other options**: OpenAI API or a local Ollama server.
- **No Vertex dependency**: inference does not use a GCP service account, Vertex IAM, or `GOOGLE_APPLICATION_CREDENTIALS`.

## Runtime notes

- **PYTHONPATH**: run commands from the repository root (see `pytest.ini` and Docker `ENV PYTHONPATH=/app`).
- **SQLite path**: set `DB_PATH` to a shared path in Docker (compose uses `/data/verdicts.db` on the `sqlite_data` volume). Verdict rows are pruned automatically on insert after `VERDICT_RETENTION_DAYS`.
- **Model credentials in Docker**: Compose reads provider keys from `.env`; no cloud credential file is mounted.
- **Docker builds**: `docker-compose.yml` defines `build:` sections (`context: .` with `agent/Dockerfile` and `api/Dockerfile`) so `docker compose up -d --build` works locally with no registry; `image:` falls back to `${REGISTRY:-infraguard}/...` for CI-pushed images.
- **Docker socket**: the agent mounts `/var/run/docker.sock` read-only; it is only used when `ENABLE_DOCKER_MONITORING=1` (`get_docker_events`, `collect_container_diagnostics`, `fetch_container_errors`). Remove the mount if you keep monitoring disabled. `:ro` on the socket is not a full security boundary.
- **env_file caveat**: docker compose `env_file` does **not** strip inline comments — `FLAG=1  # comment` becomes the literal value `1  # comment`. Keep comments on their own lines in `.env`.
- **Auth**: Only `/health` and `/login` are public. All other API and dashboard routes require an active session cookie. Failed logins re-serve the login page with the error injected server-side.
- **Staleness**: `/status` returns `age_seconds` and `stale` (true when the latest verdict is older than 3× the heartbeat interval); the dashboard shows a warning banner when stale.
