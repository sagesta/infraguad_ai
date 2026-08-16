# Disk space is running low

Case ID: RB-01
Category: Infrastructure

## When to use this runbook

Use this when a filesystem is above 85%, free space is falling quickly, or the agent reports a disk-capacity condition. Treat a full root filesystem as urgent because it can stop containers, logging, and database writes at the same time.

## First checks

1. Run `df -h` and identify the affected mount.
2. Run `df -i` to rule out inode exhaustion.
3. Use `sudo du -xhd1 /var | sort -h` and then inspect the largest directory.
4. Run `docker system df` to measure images, build cache, and volumes. Do not prune yet.

## Likely causes

- Docker JSON logs or application logs are growing without rotation.
- Old images and build cache have accumulated.
- The SQLite verdict database is not being pruned.
- A backup, export, or temporary file was left on the host.

## Remediation

Free space from a known source first. Rotate an oversized log, remove an identified temporary file, or delete a confirmed-unused image. Before removing Docker volumes, verify that they are not the PostgreSQL, Redis, SQLite, ChromaDB, or Ollama data volumes. Avoid broad commands such as `docker system prune --volumes` on this host.

If `verdicts.db` is growing unexpectedly, confirm `VERDICT_RETENTION_DAYS` is set and inspect pruning behaviour before deleting any database file.

## Validation

Run `df -h` again, confirm the affected filesystem is below the alert threshold, and watch its growth for at least two heartbeat cycles. Check that DevPlanner and InfraGuard remain healthy.

## Escalate when

Escalate if the filesystem is above 95%, becomes read-only, or returns above 85% within a day. Fast regrowth usually indicates a leak rather than routine housekeeping.

## Safe practice drill

On a practice host, create a bounded temporary file with `mkdir -p /tmp/infraguard-drill && fallocate -l 100M /tmp/infraguard-drill/disk-test.bin`. Observe the metric and ask the Runbook Assistant how to investigate disk growth. Remove it with `rm /tmp/infraguard-drill/disk-test.bin` when finished. A 100 MB file may not cross the alert threshold; the purpose is to rehearse the checks and cleanup without filling the disk.
