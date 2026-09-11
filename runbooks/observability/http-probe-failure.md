# HTTP uptime probe is failing

Case ID: RB-10
Category: Observability

## When to use this runbook

Use this when a configured `PROBE_URLS` endpoint times out, refuses the connection, or returns an unexpected status.

## First checks

1. Run `curl -i` against the public URL from the VPS.
2. Test the local origin address, such as `http://127.0.0.1:3000` or `http://127.0.0.1:8080/health`.
3. Check the target container's health and recent logs.
4. If local works but public fails, inspect Cloudflare Tunnel health and routing.

## Likely causes

- The application container is stopped or unhealthy.
- The probe URL or path is wrong.
- Cloudflare Tunnel cannot reach the local origin.
- The endpoint now requires authentication or redirects unexpectedly.

## Remediation

Fix the narrowest confirmed cause: restore the failed service, correct the probe path, or repair the tunnel route. Keep the API bound locally when Cloudflare Tunnel is the public entry point; direct internet exposure is not required.

## Validation

Both local and public requests should return the expected status, and the next two InfraGuard checks should show the probe as healthy.

## Escalate when

Escalate if the origin is healthy but Cloudflare cannot resolve the tunnel, or if recovery requires a production rollback.

## Safe practice drill

On the practice deployment, temporarily add `http://127.0.0.1:19999/health` to `PROBE_URLS` and recreate the InfraGuard agent. The unused port should produce a controlled probe failure. Confirm that a verdict appears, ask the Runbook Assistant for the HTTP probe procedure, then remove the temporary URL and recreate the agent again. Do not perform this drill while an unrelated incident is active.
