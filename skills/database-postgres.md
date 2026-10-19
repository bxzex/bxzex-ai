---
name: database-postgres
description: Setting up and running Postgres for an app, including hosting, pooling, migrations, indexes, backups and slow queries.
---
# Postgres for an App

1. **Hosting.** For a quick start use a hosted Postgres (Neon, Supabase, a platform marketplace database, or your cloud's managed service). For local work: `docker run -d --name pg -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:16`.
2. **Connection string.** `postgres://user:pass@host:5432/dbname?sslmode=require`. Store it as `DATABASE_URL` in env, never in code. Test: `psql "$DATABASE_URL" -c 'select 1'`.
3. **Pooling.** Serverless apps open many short connections and can hit the limit. Use the provider's pooled URL (often a different host or port, such as a `-pooler` host or port 6543) for the app, and the direct URL for migrations.
4. **Migrations.** Never edit tables by hand in production. Use a tool (Prisma Migrate, Drizzle Kit, or plain numbered `.sql` files). Rules: one change per migration, commit them, run on a copy first, and split risky changes (add the column nullable, backfill, then add the constraint).
5. **Indexes.** Add an index on columns you filter, join or sort by often: `create index concurrently idx_orders_user on orders(user_id);`. Foreign keys do not get indexes automatically. Too many indexes slow writes.
6. **Find slow queries.** `explain (analyze, buffers) select ...;`. Look for `Seq Scan` on a big table, large gaps between estimated and actual rows, and high `Execution Time`. Fix with an index or a narrower query, then run explain again. `pg_stat_statements` shows the worst queries overall.
7. **Backups.** Turn on the provider's automated backups and point-in-time recovery. Also take a manual dump before risky changes: `pg_dump "$DATABASE_URL" -Fc -f backup.dump`. A backup is only real after you have restored it somewhere: `pg_restore -d test_db backup.dump`.
8. **Safety.** Use parameterized queries only, a least-privilege app user, and never run destructive SQL without a `where` and a transaction (`begin; ... ; rollback;` to preview).

**Pitfalls:** forgetting `sslmode`; running migrations from every serverless instance at once; storing money in floats (use integer cents or `numeric`); `select *` on wide tables.
