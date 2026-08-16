# Prometheus scrape target is down

Case ID: RB-07
Category: Observability

## When to use this runbook

Use this when Prometheus reports `up == 0`, InfraGuard shows Prometheus as unavailable, or a target stops producing metrics.

## First checks

1. Open the Prometheus targets page or query `up` and note the failed job and instance.
2. From the Prometheus container, request the target's metrics endpoint.
3. Check that the target container is running and listening on the expected port.
4. Review the exact scrape error before changing configuration.

## Likely causes

- The exporter or application container stopped.
- The target name or port changed after a deployment.
- Prometheus and the target are on different Docker networks.
- The metrics endpoint is slow, protected, or returning an error.

## Remediation

Restore the target service if it is genuinely down. If the service is healthy, correct the Prometheus target address or network attachment and reload Prometheus. Keep telemetry ports bound to localhost or the internal Docker network; they do not need direct public exposure.

## Validation

The target should return to `UP`, a fresh sample should appear, and InfraGuard should show the Prometheus integration as healthy after the next check.

## Escalate when

Escalate if several targets fail at once, Prometheus cannot read its configuration, or the target repeatedly drops after recovery.
