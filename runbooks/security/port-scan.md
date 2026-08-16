# Possible port scan from one IP

Case ID: RB-20
Category: Security

## When to use this runbook

Use this when InfraGuard sees at least twenty recent log lines containing `connection refused` or `SYN` for the same source IP.

## First checks

1. Confirm the source IP, destination ports, protocol, and time span in the original logs.
2. Check whether the address belongs to a vulnerability scanner or administrator.
3. Review the VPS firewall and Docker port bindings for services that should not be public.
4. Look for follow-on login attempts or successful connections.

## Likely causes

- Automated internet reconnaissance.
- An authorised security or inventory scan.
- A misconfigured service repeatedly connecting to the wrong ports.
- Docker ports unintentionally bound to every interface.

## Remediation

Close unintended public ports first. For a confirmed hostile source, review the InfraGuard CrowdSec decision; the suggested ban lasts 12 hours. A single IP ban is temporary containment, not a substitute for a restrictive firewall and localhost-only bindings behind Cloudflare Tunnel.

## Validation

Confirm only the intended public services are reachable, the decision is active when used, and the scan traffic stops without affecting legitimate clients.

## Escalate when

Escalate if the scan was followed by a successful connection, an administrative port was public, or scanning continues from many addresses.
