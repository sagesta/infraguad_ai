# Network latency or intermittent connectivity

Case ID: RB-05
Category: Infrastructure

## When to use this runbook

Use this when HTTP probes are slow, external API calls time out, or several services show intermittent connection errors without a clear application failure.

## First checks

1. Compare latency for the public URL and the local service address.
2. Use `curl -sS -o /dev/null -w "%{http_code} %{time_connect} %{time_starttransfer} %{time_total}\n"` against the affected endpoint.
3. Check Cloudflare Tunnel logs and container logs for timeouts or reconnects.
4. Confirm DNS resolution and test the upstream provider separately.

## Likely causes

- Cloudflare Tunnel reconnecting or unable to reach the local origin.
- DNS delay or resolver failure.
- VPS network contention or packet loss.
- A slow application mistaken for a network problem.

## Remediation

If the local endpoint is fast but the public endpoint is slow, focus on the tunnel and external path. If both are slow, inspect application and database latency. Restart cloudflared only after confirming it is the failing component and saving its recent logs.

## Validation

Repeat the same timed request several times. Connection and total time should remain stable, and the HTTP probe should recover for at least two cycles.

## Escalate when

Escalate if packet loss affects the whole VPS, the tunnel cannot reconnect, or multiple unrelated upstream services fail together.
