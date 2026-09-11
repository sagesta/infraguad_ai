# API latency is above the normal range

Case ID: RB-12
Category: Application

## When to use this runbook

Use this when response time rises while the API still returns successful status codes, or users report that pages and actions are slow.

## First checks

1. Measure connection, time-to-first-byte, and total time for the affected route.
2. Compare one slow route with a lightweight health endpoint.
3. Check CPU, memory, database connections, slow queries, and upstream API latency.
4. Review whether the slowdown began after a release or traffic increase.

## Likely causes

- Slow database queries or exhausted connections.
- An external provider is delaying the request path.
- CPU or memory pressure on the shared VPS.
- A worker queue is backed up.

## Remediation

Reduce the responsible workload, restore the slow dependency, or roll back a confirmed regression. Add caching or query changes only after identifying the slow operation. A blanket timeout increase can mask the problem and consume more connections.

## Validation

Measure the same route using the same method. Latency should return to its normal range without an increase in errors or queue depth.

## Escalate when

Escalate if latency affects login or data writes, database lock time grows, or the shared VPS remains resource-bound.
