# Redis is unavailable

Case ID: RB-14
Category: Application

## When to use this runbook

Use this when the application logs Redis connection errors, queued work stops, or features that depend on cache or coordination fail.

## First checks

1. Confirm the Redis container is running and inspect its health and logs.
2. From the application container, resolve the configured Redis hostname and test the port.
3. Check memory use, disk space, and restart count.
4. Verify that `REDIS_URL` uses the address valid for the current Docker network.

## Likely causes

- Redis restarted, crashed, or was OOM-killed.
- The application uses `localhost` even though Redis is in another container.
- Containers no longer share a network.
- Redis persistence or disk space has failed.

## Remediation

Restore network reachability or restart the Redis container only after capturing the reason it stopped. Correct `REDIS_URL` and recreate the affected application containers if the address is wrong. Do not delete the Redis volume unless the data-loss impact is understood.

## Validation

The application should connect without retries, queued work should resume, and Redis memory and restart count should remain stable.

## Escalate when

Escalate if Redis contains non-reconstructable data, persistence is corrupted, or it repeatedly exceeds memory.
