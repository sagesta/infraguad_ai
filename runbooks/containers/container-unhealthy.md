# Container health check is failing

Case ID: RB-16
Category: Containers

## When to use this runbook

Use this when a container remains running but Docker marks it unhealthy, or its health endpoint fails while the process still exists.

## First checks

1. Inspect the health-check output and timestamps with `docker inspect <container>`.
2. Run the health-check command inside the container.
3. Request the same endpoint from the host and from dependent containers.
4. Check whether the health-check path, port, timeout, or start period changed.

## Likely causes

- The application is running but a dependency is down.
- The health-check command or URL is incorrect.
- Startup takes longer than the configured grace period.
- The process is deadlocked or resource-starved.

## Remediation

Fix the underlying application or dependency failure. If the check itself is wrong, correct it and recreate the service. Extend the start period only when measured startup time justifies it. A restart may restore service temporarily, but capture the failure first.

## Validation

Docker should report healthy across several checks, and the endpoint should work from the same network path used by real callers.

## Escalate when

Escalate if the service passes a superficial health check while user operations still fail, or health repeatedly flips between healthy and unhealthy.
