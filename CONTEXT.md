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
connectivity = "Tailscale VPN mesh"
metrics_url = "PROMETHEUS_URL env var"
logs_url = "LOKI_URL env var"
ssh_host = "TAILSCALE_HOST env var"

[llm]
provider = "AWS Bedrock"
model = "anthropic.claude-haiku-20240307-v1:0"
client = "boto3"
output_format = "JSON — severity, summary, root_cause, recommended_action"

[agent]
framework = "LangGraph"
schedule = "60 second asyncio heartbeat loop"
severity_levels = ["ok", "warning", "high", "critical"]
notify_on = ["high", "critical"]
ssh_exec_on = ["critical"]

[mcp_tools]
loki = "fetch_loki_logs() — last 50 lines"
prometheus = "query_prometheus() — CPU, RAM, disk, error rate"
docker_events = "get_docker_events() — restarts, unhealthy containers"
http_probe = "probe_endpoints() — status + latency"
ssh_exec = "execute_remote_command() — Paramiko over Tailscale"
notify = "send_push_notification() — ntfy.sh"

[api]
framework = "FastAPI"
storage = "SQLite via aiosqlite"
endpoints = ["/status", "/alerts", "/health"]

[dashboard]
type = "Single HTML page"
refresh_interval = "30 seconds"
served_by = "FastAPI static"

[notifications]
provider = "ntfy.sh"
topic = "NTFY_TOPIC env var"
priority_map = { ok = "min", warning = "default", high = "high", critical = "urgent" }

[env_vars]
required = ["LOKI_URL", "PROMETHEUS_URL", "TAILSCALE_HOST", "SSH_USER", "SSH_KEY_PATH", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION", "NTFY_TOPIC", "PROBE_URLS"]

[testing]
framework = "pytest + respx"
test_files = ["tests/test_tools.py", "tests/test_agent.py"]
```

## Runtime notes

- **PYTHONPATH**: run commands from the `infraguard-ai/` directory (see `pytest.ini` and `Dockerfile` `ENV PYTHONPATH=/app`).
- **SQLite path**: set `DB_PATH` to a shared path in Docker (compose uses `/data/verdicts.db`).
- **SSH key in Docker**: mount the private key into the container and point `SSH_KEY_PATH` at the in-container path (never commit keys).
- **Docker events**: optional; set `DOCKER_HOST` (for example `unix:///var/run/docker.sock`) and mount the socket if you want live Docker events inside the agent container.
