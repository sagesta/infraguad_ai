# Disk space running low

## Symptoms
Prometheus reports disk usage above 85% on the root or /var partition, or the
agent's verdict flags a `prometheus:disk-low:/` condition.

## First checks
1. `df -h` to confirm which mount is filling up.
2. `du -sh /var/log/* | sort -rh | head` — application and Docker logs are
   the usual cause on this stack.
3. `docker system df` — old images and stopped containers accumulate over
   time if pruning isn't scheduled.

## Resolution
- Rotate or truncate oversized logs under `/var/log`.
- `docker system prune -af --volumes` if disk space is critical and no
  in-progress builds depend on cached layers (destructive — confirm first).
- If the growth is from the SQLite verdicts database, confirm
  `VERDICT_RETENTION_DAYS` is set and verdicts are actually being pruned on
  insert (`api/store.py`).

## When to escalate
If usage returns to >85% within a day of cleanup, the growth rate points to
a leak (a service writing logs faster than expected) rather than routine
accumulation — investigate the writing process directly.
