# Repeated HTTP 401 or 403 responses from one IP

Case ID: RB-18
Category: Security

## When to use this runbook

Use this when the threat panel reports an HTTP brute-force pattern. InfraGuard raises this pattern when the same source IP appears in at least ten recent log lines containing HTTP 401, HTTP 403, or `unauthorized`.

## First checks

1. Confirm the IP, request count, time window, path, and user agent in Loki.
2. Check whether the address belongs to a trusted proxy, uptime service, office, or test runner.
3. Look for successful login or sensitive requests from the same IP after the failures.
4. Verify that the log line contains the real client IP rather than the Cloudflare or reverse-proxy address.

## Likely causes

- Credential guessing or a scripted login attack.
- A client with an expired credential retrying too aggressively.
- A test or integration using an old secret.
- Incorrect proxy logging that attributes many users to one address.

## Remediation

For a confirmed malicious source, the operator may use InfraGuard's threat action to submit a CrowdSec IP ban. The default suggested duration is 24 hours. Review the generated IP, reason, and duration before applying it. If CrowdSec is not configured, the same action is recorded as a dry run and no firewall change occurs.

Fix compromised credentials separately; an IP ban alone does not secure an exposed account. Do not ban a shared proxy or Cloudflare edge address.

## Validation

Confirm the CrowdSec decision exists when live mode is intended, the targeted requests stop, and legitimate login traffic still works. Record why the decision was made.

## Escalate when

Escalate if any login succeeded, several IPs are involved, privileged accounts were targeted, or the logs do not preserve the real client address.

## Safe practice drill

Emit twelve synthetic container log lines containing the documentation-only IP `192.0.2.123` and status `401`. Wait for Loki ingestion, open Threat Detection, and verify that InfraGuard reports the IP and count. Review the proposed decision but do not apply it while CrowdSec is in live mode. The synthetic lines will age out of the scan window; no production account is touched.
