# InfraGuard AI Runbook and Practice Guide

This guide accompanies the 20 Markdown cases under `runbooks/`. The files are the local knowledge base used by the dashboard's Runbook Assistant. Their subdirectories become retrieval categories, and the first heading in each file becomes its source title.

## Runbook catalogue

| ID | Case | Category |
|---|---|---|
| RB-01 | Disk space is running low | Infrastructure |
| RB-02 | CPU saturation on the host | Infrastructure |
| RB-03 | Memory pressure or out-of-memory risk | Infrastructure |
| RB-04 | High load average with unclear cause | Infrastructure |
| RB-05 | Network latency or intermittent connectivity | Infrastructure |
| RB-06 | DNS resolution failure | Infrastructure |
| RB-07 | Prometheus scrape target is down | Observability |
| RB-08 | Loki has stopped receiving logs | Observability |
| RB-09 | Prometheus metrics are stale | Observability |
| RB-10 | HTTP uptime probe is failing | Observability |
| RB-11 | Spike in HTTP 5xx responses | Application |
| RB-12 | API latency is above the normal range | Application |
| RB-13 | PostgreSQL connection pool is exhausted | Application |
| RB-14 | Redis is unavailable | Application |
| RB-15 | Container is restarting repeatedly | Containers |
| RB-16 | Container health check is failing | Containers |
| RB-17 | Service regression after deployment | Containers |
| RB-18 | Repeated HTTP 401 or 403 responses from one IP | Security |
| RB-19 | Repeated SSH authentication failures | Security |
| RB-20 | Possible port scan from one IP | Security |

## How remediation works in the app

InfraGuard separates diagnosis from change execution.

1. On each heartbeat, the agent collects Loki logs, Prometheus metrics, HTTP probe results, and optional Docker context.
2. The selected model returns a structured verdict: severity, summary, likely root cause, recommended action, and a stable condition signature.
3. InfraGuard stores the verdict. For high or critical severity it can collect extra Docker diagnostics and send an ntfy notification.
4. The operator reviews the evidence and follows the relevant local runbook. Service restart, rollback, scaling, disk cleanup, database work, and configuration changes remain manual actions.
5. Threat response is the sole corrective action exposed by the application. After a deterministic log pattern is detected, an operator may approve a server-generated CrowdSec IP-ban decision. It is a dry run when CrowdSec is not configured and a live ban when it is configured.

The **Mark known** action is not remediation. It records that an operator has reviewed an unchanged low-risk condition and hides matching acknowledged items from the default history view. The model still evaluates later heartbeat data, and a changed condition, prompt version, or model produces a new fingerprint.

This boundary is deliberate: the LLM recommends action, but it cannot restart DevPlanner, delete files, alter the database, or change the firewall by itself.

## Prepare the runbook index

After deploying these files on the VPS:

1. Confirm `./runbooks` is mounted read-only at `/app/runbooks` in the API container.
2. Open the InfraGuard dashboard and select **Re-index** in the Runbook Assistant.
3. Confirm that the response reports 20 documents indexed.
4. Ask a simple grounding question, such as: `What should I check before cleaning Docker disk usage?`
5. Verify that the answer cites **Disk space is running low**. The wording may vary by model, but the actions should come from the runbook.

## Five controlled practice cases

Run these only when the VPS is otherwise healthy and no real incident is active. Take a screenshot of the starting dashboard, note the heartbeat time, and perform one exercise at a time. Each drill has a clear rollback.

### Practice 1 — Disk investigation and retrieval

Goal: rehearse the disk runbook without filling the VPS.

1. Record `df -h` and `docker system df`.
2. Create a bounded file: `mkdir -p /tmp/infraguard-drill && fallocate -l 100M /tmp/infraguard-drill/disk-test.bin`.
3. Ask the assistant: `Disk usage is rising on /var. What should I inspect before deleting anything?`
4. Confirm the answer recommends measuring the affected mount, large directories, logs, and Docker usage before cleanup.
5. Remove the file: `rm /tmp/infraguard-drill/disk-test.bin`.
6. Run `df -h` again and record the result.

Expected evidence: a grounded assistant answer citing RB-01. The file is intentionally too small to guarantee a Prometheus threshold alert.

### Practice 2 — Failed HTTP probe

Goal: exercise a real heartbeat verdict with a reversible configuration change.

1. Save the current `PROBE_URLS` value.
2. Append `http://127.0.0.1:19999/health`, an intentionally unused local port.
3. Recreate the InfraGuard agent with `docker compose up -d --force-recreate agent`.
4. Wait for the next heartbeat and record the probe failure and verdict.
5. Ask the assistant: `The public site works, but one configured HTTP probe is refusing connections. What should I check?`
6. Restore the original `PROBE_URLS` and recreate the agent again.
7. Confirm the probe returns to healthy on the next cycle.

Expected evidence: a failed probe, a stored verdict, a grounded RB-10 answer, and a healthy recovery after rollback.

### Practice 3 — Synthetic HTTP 500 logs

Goal: test Loki ingestion and incident reasoning without making DevPlanner return errors.

1. Run this disposable log producer on the VPS:

   `docker run --name infraguard-drill-500 alpine:3.20 sh -c 'i=1; while [ $i -le 15 ]; do echo "192.0.2.10 - - [drill] GET /api/tasks HTTP/1.1 500"; i=$((i+1)); done'`

2. Confirm the synthetic lines appear in Loki.
3. Wait for a heartbeat, then inspect the verdict and ask: `What is the runbook for a sudden HTTP 500 spike after deployment?`
4. Remove the stopped producer with `docker rm infraguard-drill-500`.

Expected evidence: Loki lines, a model verdict when those lines fall inside the collection window, and an answer citing RB-11. The exercise does not send a failing request to DevPlanner.

### Practice 4 — Disposable container restart loop

Goal: exercise optional Docker event monitoring and the restart-loop procedure.

1. Confirm `ENABLE_DOCKER_MONITORING=1` and that the InfraGuard agent has read-only access to the Docker socket.
2. Run `docker run -d --name infraguard-drill-restart --restart on-failure:3 alpine:3.20 sh -c "echo drill restart; exit 1"`.
3. Inspect its status, exit code, restart count, and logs.
4. Wait for the next InfraGuard check and ask the assistant how to investigate a restart loop.
5. Remove it with `docker rm infraguard-drill-restart` after it has stopped.

Expected evidence: Docker restart events or diagnostics and a grounded answer citing RB-15. If Docker monitoring is disabled, document that the runbook retrieval works while event detection is out of scope for that configuration.

### Practice 5 — Synthetic HTTP brute-force pattern

Goal: demonstrate deterministic threat detection and the approval boundary.

1. Run:

   `docker run --name infraguard-drill-401 alpine:3.20 sh -c 'i=1; while [ $i -le 12 ]; do echo "192.0.2.123 - - [drill] GET /login HTTP/1.1 401 0"; i=$((i+1)); done'`

2. Confirm all twelve lines reach Loki.
3. Open Threat Detection and verify that InfraGuard reports the documentation-only address `192.0.2.123` after the next scan.
4. Inspect the proposed CrowdSec decision. Do **not** apply it when CrowdSec is in live mode; the purpose is to demonstrate that an operator must approve the action.
5. Remove the stopped producer with `docker rm infraguard-drill-401`.
6. Wait for the synthetic lines to age out of the threat scanner's recent-log window.

Expected evidence: one `http_brute_force` finding with a count of at least 10 and a proposed 24-hour IP ban. No ban is created unless the operator explicitly submits it.

## What to record for the project evaluation

For each practice case, capture the ground-truth condition, telemetry shown to the model, verdict severity, root-cause assessment, recommended action, schema validity, latency, token use if available, retrieved runbook sources, and whether the recovery check passed. Also record false positives and any action the model recommended that was not supported by the runbook. This gives Chapter Five evidence about both the reasoning pipeline and the human-approval boundary.
