# Memory pressure or out-of-memory risk

Case ID: RB-03
Category: Infrastructure

## When to use this runbook

Use this when available memory is low, swap activity rises, containers are killed, or the kernel reports an out-of-memory event.

## First checks

1. Run `free -h` and note available memory and swap use.
2. Run `ps -eo pid,comm,rss,%mem --sort=-rss | head`.
3. Run `docker stats --no-stream` and identify containers whose memory is growing.
4. Check recent kernel messages with `journalctl -k --since "30 minutes ago" | grep -i -E "oom|out of memory|killed process"`.

## Likely causes

- An application or worker memory leak.
- Too many concurrent processes or model requests.
- Local Ollama competing with the application for RAM.
- Missing or ineffective container memory limits.

## Remediation

Reduce the workload or stop a confirmed non-essential process. Capture logs and memory figures before restarting a leaking container. If Ollama is not in use, stop that service to return memory to DevPlanner. Add or adjust container limits only after measuring normal peak use; a limit that is too low can create repeated restarts.

## Validation

Available memory should stabilise, swap activity should fall, and no new OOM messages should appear over several heartbeat cycles.

## Escalate when

Escalate if the database is being killed, multiple containers are affected, or memory continues to grow after the responsible workload is stopped.
