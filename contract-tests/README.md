# contract-tests

A shared, language-agnostic test suite that runs against any running
implementation of the API in `spec/spec.yaml` over plain HTTP. Every
per-language directory should be able to pass this suite unmodified - it's
the proof that an implementation is behaviorally equivalent to the others,
not just "the endpoints exist."

There are two complementary halves:

- **`test_lifecycle.py`** - deterministic, hand-written end-to-end flows
  (create a project, add an issue, comment on it, assign a user, archive the
  project, etc.), asserting on the actual documented business behavior:
  status codes, state-machine transitions (409 on invalid transitions),
  idempotency, and things the spec can't express in JSON Schema alone (e.g.
  a webhook's `secret` must never come back in a response). This is the file
  to read first when starting a new language implementation - it's the
  reference "golden path."
- **`test_schema.py`** - property-based fuzzing via
  [Schemathesis](https://schemathesis.readthedocs.io/), generating requests
  for every operation in the spec and checking the server never 500s and
  that responses match their declared schema. This catches contract drift a
  hand-written test wouldn't (wrong field types, undocumented fields,
  content-type mismatches).

## Why direct DB access

The spec has no endpoint to create a `users` row - every implementation is
expected to resolve identity from the API key out-of-band. Since every
language implementation shares the same Postgres instance (see `/infra`),
`conftest.py`'s `seeded_user` fixture inserts a row directly via
`DATABASE_URL` so tests can exercise `author_id` / assignee fields without
depending on any one implementation's auth internals. This is the only place
the suite talks to anything other than the HTTP API.

## Running

```sh
./contract-tests/run.sh
```

This creates a local `.venv`, installs `requirements.txt`, and runs pytest.
Pass extra pytest args straight through, e.g.:

```sh
./contract-tests/run.sh test_lifecycle.py -v
./contract-tests/run.sh test_schema.py --hypothesis-seed=0
```

Configure via env vars (all optional, defaults match local dev):

| Var | Default |
| --- | --- |
| `CONTRACT_TEST_BASE_URL` | `http://localhost:8080/v1` |
| `CONTRACT_TEST_API_KEY` | `dev-local-key` |
| `DATABASE_URL` | `postgres://polyglot:polyglot@localhost:5432/polyglot_api?sslmode=disable` |

The target implementation must already be running (`infra/`'s Postgres up,
migrations applied, the app started and listening on the spec's base URL)
before you run this.

## A note on `test_schema.py` and status codes

`test_schema.py` deliberately does not check `status_code_conformance`. The
spec documents the "interesting" error responses per operation
(401/404/409/422) but doesn't enumerate every generic 400 an input validator
can produce (e.g. a malformed enum value, an out-of-range limit). Fuzzing
will legitimately hit those - they're not contract violations, just gaps in
how exhaustively the spec documents input validation. If that bothers you,
the fix is to add those responses to `spec/spec.yaml`, not to loosen an
implementation.

What *is* checked, and should never fail: **no 500s**, and **response bodies
match their declared schema**. Both of these already caught real bugs during
the TypeScript implementation (an empty `?cursor=` 400ing instead of being
treated as absent, and an embedded NUL byte in a string field causing an
uncaught Postgres error) - treat any new failure here as a real
implementation bug, not fuzzer noise, until proven otherwise.
