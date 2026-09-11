# CPU saturation on the host

Case ID: RB-02
Category: Infrastructure

## When to use this runbook

Use this when CPU use remains high for several minutes, load climbs, or API latency rises at the same time as CPU consumption.

## First checks

1. Run `uptime` and compare load average with the number of CPU cores from `nproc`.
2. Run `top` or `ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head` to find the busiest processes.
3. Run `docker stats --no-stream` to identify the responsible container.
4. Compare the start of the spike with deployments, scheduled jobs, and traffic changes.

## Likely causes

- A request loop, expensive query, or runaway worker.
- A new release increased processing cost.
- Too many concurrent jobs or AI requests.
- The VPS is undersized for DevPlanner and InfraGuard running together.

## Remediation

Pause or rate-limit the specific workload if that can be done safely. If a single container is unhealthy, capture its logs and current resource use before restarting it. Roll back only when the spike clearly began with a release and the previous image is known to be healthy. Do not restart every container at once; that erases useful evidence and creates a wider outage.

## Validation

CPU and load should return to the normal range, request latency should recover, and the same process should not immediately climb again. Confirm both application health endpoints.

## Escalate when

Escalate if load continues to rise, the host stops accepting connections, or CPU remains saturated after the suspected workload is stopped.
