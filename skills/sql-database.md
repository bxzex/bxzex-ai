---
name: sql-database
description: Designing database tables or writing and fixing SQL queries.
---
# SQL and databases

**Before writing a query**
Look at the real schema: table names, columns, types, keys. Do not guess column names.

**Designing tables**
- One table per kind of thing. One row per thing.
- Every table has a primary key.
- Store each fact once. Link tables with foreign keys instead of copying data.
- Pick real types: dates as dates, money as decimal or integer cents, never floats.
- Add `created_at`. Add `NOT NULL` wherever a value is always required.
- Index the columns you filter and join on.

**Writing queries**
- Name the columns you need. Avoid `SELECT *` in real code.
- Join on keys, and say which join you mean. A missing join condition multiplies rows.
- Filter early. Add a `LIMIT` while exploring.
- `NULL` is not equal to anything, including itself. Use `IS NULL`.
- With `GROUP BY`, every selected column is either grouped or aggregated.
- Check the row count of the result against what you expect. Double counting from a join is the most common wrong answer.

**Safety**
- Always pass values as parameters. Never build SQL by gluing in user text.
- Before `UPDATE` or `DELETE`, run the same `WHERE` as a `SELECT` and look at the rows.
- Wrap changes in a transaction so they can be rolled back.
- Never run a destructive statement or a migration on real data without the user's clear yes and a backup.

Explain what the query returns in one sentence, and say which database it is written for.
