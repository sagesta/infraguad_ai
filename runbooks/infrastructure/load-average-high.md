# High load average with unclear cause

Case ID: RB-04
Category: Infrastructure

## When to use this runbook

Use this when load average is high but CPU use alone does not explain it. High load can also mean processes are waiting for disk or other resources.

## First checks

1. Run `uptime` and `nproc` to put the load number in context.
2. In `top`, check process state and the CPU wait value (`wa`).
3. Run `vmstat 1 5` and look for blocked processes, swap, and I/O wait.
4. Check disk capacity, database health, and container restart counts.

## Likely causes

- Slow or saturated disk I/O.
- Memory pressure and swapping.
- A blocked database or network dependency.
- Many short-lived processes or a restart loop.

## Remediation

Treat the underlying bottleneck rather than the load number. Free disk space, reduce the job queue, restore the failed dependency, or stop the confirmed runaway process. Preserve logs before restarting a service.

## Validation

The one-minute load should begin falling first, followed by the five- and fifteen-minute values. API latency and probe results should recover at the same time.

## Escalate when

Escalate if the host is unresponsive, blocked processes keep increasing, or the cause is storage failure rather than temporary contention.
