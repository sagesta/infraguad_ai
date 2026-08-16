# Service regression after deployment

Case ID: RB-17
Category: Containers

## When to use this runbook

Use this when errors, latency, restarts, or missing functionality begin soon after a new image or configuration is deployed.

## First checks

1. Record the deployment time, image tag or digest, and changed configuration.
2. Compare health, logs, and key requests before and after that time.
3. Confirm whether the failure affects one service or the whole stack.
4. Verify that the previous image is still available and its database compatibility is understood.

## Likely causes

- A code defect or incompatible dependency.
- A missing environment value or mount.
- A database migration is incomplete or incompatible with rollback.
- The new image requires more CPU or memory.

## Remediation

Correct a simple configuration mistake when the intended value is certain. Otherwise, roll back the affected service to the last verified image using the project's deployment procedure. Do not roll back across a destructive database migration without a separate data plan.

## Validation

Repeat the failed user path, confirm health and error rates recover, and record the image now running. Keep the incident open long enough to see that the failure does not recur.

## Escalate when

Escalate if data may have been written in an incompatible format, more than one release must be reversed, or the rollback image is unavailable.
