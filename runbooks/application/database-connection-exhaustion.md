# PostgreSQL connection pool is exhausted

Case ID: RB-13
Category: Application

## When to use this runbook

Use this when the API logs pool timeouts, PostgreSQL reports too many clients, or requests wait for database connections.

## First checks

1. Count current connections by application and state in `pg_stat_activity`.
2. Look for long-running, idle-in-transaction, and blocked sessions.
3. Compare the application's pool limit with PostgreSQL's connection limit.
4. Check whether a deployment or worker increase multiplied the number of pools.

## Likely causes

- Connections are leaked or transactions are left open.
- Pool size is too large across several application processes.
- A slow query holds connections for too long.
- PostgreSQL is unhealthy and connections are not completing.

## Remediation

Stop the specific runaway workload and fix the leaking or slow request path. Terminate database sessions only when their owner and impact are understood. Tune the application pool before increasing PostgreSQL's global limit; simply raising the limit can move the failure to memory exhaustion.

## Validation

Pool wait time should fall, connection count should remain below the limit, and normal requests should complete without pool timeout errors.

## Escalate when

Escalate if sessions are blocking data migrations, writes may be incomplete, or the database itself is unstable.
