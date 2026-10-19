---
name: testing
description: Writing, running and fixing automated tests for a project, using the test runner it already has.
---
# Testing

1. **Find the runner.** Do not add a new one. Check:
   - `package.json` scripts and devDependencies: vitest, jest, mocha.
   - `pyproject.toml`, `pytest.ini`, `tox.ini`: pytest.
   - `go.mod`: `go test ./...`.
   - Cargo.toml: `cargo test`.
   Look at where existing tests live and copy their naming and style.
2. **Run what exists first.** `npm test`, `pytest -q`, `go test ./...`. Note which already fail so you do not take the blame for them.
3. **Test behavior, not internals.** Call the public function or endpoint and check the output or visible effect. Do not assert on private helpers, call counts or exact internal structure unless that is the contract.
4. **Per function, cover:**
   - the normal case with realistic input
   - empty input, zero, one item, many items
   - boundaries (off by one, max length, negative numbers)
   - bad input and the expected error
   - one case that previously broke, if this is a bug fix (write the failing test first, see it fail, then fix)
5. **Name tests as sentences:** `test_rejects_expired_token`, `it("returns 404 for unknown id")`.
6. **Keep tests independent.** No shared state between tests, no order dependence, temp files in a temp dir (`tmp_path` in pytest), fake the clock and the network. Never hit real paid APIs or production data.
7. **Run them.** Single file: `pytest tests/test_x.py -q`, `npx vitest run path`, `go test ./pkg -run TestName -v`. Then the whole suite.
8. **Fix flaky tests.** Run the test 20 times: `for i in $(seq 20); do pytest -q tests/test_x.py || break; done`. Common causes: real time, random values without a seed, sleeps instead of waiting for a condition, shared files or ports, test order. Fix the cause. Do not just add a retry.

Pitfalls: tests that pass when the code is broken (check by breaking the code on purpose for a moment), asserting nothing, copying the implementation into the test, huge snapshot files nobody reads.

Report the command you ran and the pass and fail counts you saw.
