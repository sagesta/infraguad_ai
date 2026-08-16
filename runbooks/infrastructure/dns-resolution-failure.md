# DNS resolution failure

Case ID: RB-06
Category: Infrastructure

## When to use this runbook

Use this when logs contain `name or service not known`, `temporary failure in name resolution`, or similar errors for Gemini, Anthropic, OpenAI, ntfy, or monitored URLs.

## First checks

1. Resolve the hostname from the VPS with `getent hosts <hostname>`.
2. Repeat the lookup inside the affected container.
3. Inspect `/etc/resolv.conf` on the host and in the container.
4. Test a known hostname to distinguish one bad record from a resolver outage.

## Likely causes

- A wrong hostname in `.env`.
- The host resolver is unavailable.
- Docker DNS is unhealthy.
- The upstream DNS record was removed or has not propagated.

## Remediation

Correct a confirmed hostname typo and recreate only the affected container so it receives the new environment. For a resolver outage, restore the host's configured resolver before restarting application services. Do not replace DNS settings globally based on a single failed lookup.

## Validation

Resolve the hostname both on the host and in the container, then repeat the original request. Confirm the failure disappears from new logs.

## Escalate when

Escalate if all containers lose DNS, the host resolver repeatedly fails, or a public DNS change is required.
