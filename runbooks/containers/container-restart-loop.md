# Container is restarting repeatedly

Case ID: RB-15
Category: Containers

## When to use this runbook

Use this when Docker reports repeated restarts, the service never becomes healthy, or InfraGuard's Docker event monitor reports a restart loop.

## First checks

1. Run `docker ps -a` and note the status, exit code, and restart count.
2. Read the previous attempt with `docker logs --tail 200 <container>`.
3. Inspect the container's health result and configured restart policy.
4. Check recent image, environment, volume, and command changes.

## Likely causes

- The process exits because configuration or a secret is missing.
- A dependency is unavailable during startup.
- The health check is wrong or the startup period is too short.
- The image entry point fails or the container is OOM-killed.

## Remediation

Stop the restart storm if it is consuming resources, then correct the specific startup error. Recreate the one service with the intended image and environment. Roll back when a new image is the confirmed cause. Do not keep increasing the restart delay without resolving the exit.

## Validation

The restart count should stop increasing, the health status should become healthy, and the service should answer its normal local health request.

## Escalate when

Escalate if the database container is involved, the previous image also fails, or a volume appears damaged.

## Safe practice drill

With Docker monitoring enabled, run `docker run -d --name infraguard-drill-restart --restart on-failure:3 alpine:3.20 sh -c "echo drill restart; exit 1"`. Watch the Docker event and dashboard history, then inspect the container's exit and logs. Clean up with `docker rm infraguard-drill-restart` after it stops. This container has no application volume or network dependency.
