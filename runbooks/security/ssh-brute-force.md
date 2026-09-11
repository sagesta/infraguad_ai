# Repeated SSH authentication failures

Case ID: RB-19
Category: Security

## When to use this runbook

Use this when the threat panel reports at least ten recent `failed password` or `authentication failure` log lines from one IP.

## First checks

1. Confirm the source IP, usernames, count, and timestamps in the original authentication logs.
2. Search for a successful login from the same IP.
3. Check whether the source belongs to an administrator or automation host.
4. Confirm SSH is using key authentication and that password login is disabled where appropriate.

## Likely causes

- Internet-wide password scanning.
- A compromised key or credential being tested.
- A legitimate administrator using a stale key or wrong account.
- A monitoring or automation job with outdated credentials.

## Remediation

For a confirmed hostile IP, review and apply the InfraGuard CrowdSec decision; the suggested SSH ban lasts 48 hours. Revoke affected credentials and review `authorized_keys` if a successful login occurred. Restrict SSH at the network layer and prefer key-only authentication. Do not lock out the only verified administration path during an active incident.

## Validation

Check that the decision is active, failed attempts fall, and an authorised administrator can still connect through the approved path.

## Escalate when

Escalate immediately if there was a successful login, a privileged account was targeted, or system files and keys may have changed.
