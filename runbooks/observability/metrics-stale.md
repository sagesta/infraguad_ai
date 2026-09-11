# Prometheus metrics are stale

Case ID: RB-09
Category: Observability

## When to use this runbook

Use this when Prometheus responds but values no longer change, timestamps are old, or InfraGuard reaches Prometheus yet receives misleadingly quiet data.

## First checks

1. Query `time() - timestamp(up)` and inspect the age of the latest samples.
2. Check scrape duration and scrape errors for the affected target.
3. Compare the target's `/metrics` output with the value stored by Prometheus.
4. Confirm the VPS clock and container time are correct.

## Likely causes

- Prometheus is running but scrapes are failing.
- An exporter is serving cached or frozen values.
- Clock drift makes fresh samples look old or future-dated.
- A recording rule or dashboard query uses the wrong time range.

## Remediation

Restore fresh scraping at the source. Restart an exporter only after confirming its own values are frozen. Correct time synchronisation on the host if timestamps are wrong. Do not delete Prometheus data merely because a query is stale.

## Validation

Sample timestamps should advance on each scrape and values should respond to a harmless, known change in load.

## Escalate when

Escalate if stored series are corrupted, the host clock cannot remain synchronised, or stale metrics affected an incident decision.
