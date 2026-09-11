# Loki has stopped receiving logs

Case ID: RB-08
Category: Observability

## When to use this runbook

Use this when recent log queries are empty, threat detection scans zero lines unexpectedly, or the Loki status chip turns unavailable while applications are still producing logs.

## First checks

1. Query Loki for a broad recent window and then for a known container label.
2. Check the latest timestamp returned; distinguish an ingestion gap from a quiet application.
3. Inspect Loki and the log collector (Alloy or Promtail) container logs.
4. Confirm the collector can read Docker logs and reach Loki on the shared network.

## Likely causes

- Alloy or Promtail stopped or lost access to Docker logs.
- Loki is unhealthy, out of disk space, or rejecting writes.
- Labels changed and the current query no longer matches.
- `LOKI_URL` points at the wrong host or port.

## Remediation

Correct the broken collector-to-Loki path. Recreate only the failed component after saving its error output. If labels changed, update the InfraGuard query to match the labels actually stored rather than broadening it without limit.

## Validation

Generate one harmless application request, confirm its log arrives with a current timestamp, and verify that the dashboard's Loki status becomes healthy.

## Escalate when

Escalate if Loki reports storage corruption, writes fail because the disk is full, or the gap covers logs needed for an active incident.
