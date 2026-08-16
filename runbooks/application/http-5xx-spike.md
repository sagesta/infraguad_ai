# Spike in HTTP 5xx responses

Case ID: RB-11
Category: Application

## When to use this runbook

Use this when server-error responses rise above the normal baseline, an endpoint begins returning 500-series responses, or logs show repeated unhandled exceptions.

## First checks

1. Identify the first affected time, route, and application version.
2. Group recent errors by status code, route, and exception rather than reading isolated lines.
3. Check database, Redis, and upstream API health.
4. Compare the start of the spike with the most recent deployment or configuration change.

## Likely causes

- A release introduced an application error.
- PostgreSQL, Redis, or an external API is unavailable.
- A required environment value is missing.
- Resource pressure is causing timeouts or failed requests.

## Remediation

Restore the failed dependency or correct the confirmed configuration error. If the errors began immediately after a release and the previous image is known-good, use the project's rollback procedure. Capture the exception and affected request before restarting anything. Do not hide the incident by changing the endpoint to return 200.

## Validation

The error ratio should return to baseline, the affected route should succeed, and no new matching exception should appear over several minutes.

## Escalate when

Escalate if errors affect writes or authentication, data integrity is uncertain, or no safe rollback image is available.

## Safe practice drill

Generate synthetic log evidence without breaking DevPlanner: run a disposable container that writes at least twelve lines containing a documentation-only IP and an HTTP 500 status, then exits. Confirm the log collector sends those lines to Loki and ask the Runbook Assistant for the 5xx procedure. This rehearses retrieval and log inspection; it does not change real application traffic. Remove the disposable container after the logs have been observed.
