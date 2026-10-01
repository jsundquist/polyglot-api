# Project Brief: polyglot-api

**Repo name:** `polyglot-api`

**Description:** Same OpenAPI-spec'd issue-tracking API, implemented in C#, TypeScript, Python, and Go (Rust optional/stretch) to compare language and framework tradeoffs.

## Goal

Jonathan is a long-time single-language (C#/.NET, frontend-through-platform-engineering) developer branching into new languages to:

1. Genuinely learn them
2. Understand *why* you'd reach for one over another
3. Demonstrate rapid ramp-up ability for a Principal/Staff-level job search

The code itself is secondary to the *learning artifact* — documentation of the ramp-up process matters as much as the working implementations.

## Domain: Issue Tracker

Chosen over a generic Petstore-style spec for relational depth and a natural fit with Jonathan's platform-engineering/IDP background.

Core entities: projects, issues, labels, assignees, comments, and webhook delivery on state change (issue created/updated/status-changed).

Enough complexity to make the connector layer (below) do real work — real joins, a state machine (issue: open → in-progress → closed, etc.), and an outbound webhook connector for retry/backoff comparison.

## Structure — single monorepo, NOT branch-per-language

```
/spec/                  ← single source-of-truth OpenAPI spec (yaml)
/contract-tests/        ← shared black-box test suite (e.g. Schemathesis or Newman) run against every implementation
/infra/                 ← shared docker-compose.yml (Postgres, Redis, etc.)
/csharp/
/typescript/
/python/
/go/
/rust/                  ← optional/stretch
/docs/                  ← comparison notes, ADRs on language/framework tradeoffs
/README.md              ← landing page + comparison table (language, framework, ORM/connector choices, status, "days to first passing contract test")
```

**Rationale:** shared spec/infra without duplication or branch drift; one contract-test suite proves behavioral equivalence across all implementations; CI can matrix per-language directory; README doubles as a portfolio comparison table.

## Language + framework lineup, in build order

1. **C#** — ASP.NET Core, EF Core. Reference/control implementation (already fluent).
2. **TypeScript** — **NestJS** (not Express/Fastify — deliberately chosen for DI/decorator/module architecture, directly comparable to ASP.NET Core, and because NestJS shows up explicitly in job postings Jonathan is targeting).
3. **Python** — **FastAPI** (Pydantic validation, async, auto OpenAPI docs, dominant in current job postings; acknowledged tradeoff that its DI is function-based `Depends()` rather than container-based like Nest/ASP.NET Core).
4. **Go** — idiomatic minimal stack: `net/http` + chi (or similar). Deliberately NOT framework-heavy — doubling up or over-engineering here works against Go's own philosophy.
5. **Rust** (optional/stretch) — Axum, if time allows. Stretch language for genuine "different thinking" (ownership, explicit error handling).

Explicitly decided **against** building multiple framework variants per language (e.g., NestJS+Fastify, FastAPI+Litestar) — that idea serves an architecture-comparison goal, not the ramp-up/learning-speed goal, and would eat into time better spent on new languages.

## Connector layer

This is where the real learning/comparison happens — prioritize over polishing the API surface.

Each language implementation should include 2–3 backend connectors to compare idiomatic patterns:

- **Relational DB** (Postgres) — via each language's typical ORM/query layer (EF Core, NestJS+TypeORM/Prisma, SQLAlchemy async, sqlc/GORM, SQLx for Rust)
- **Async/networked store** (Redis) — for caching or event/queue patterns
- **Outbound HTTP connector** (webhook delivery on issue state change) — to compare retry/backoff/resilience patterns (Polly in C#, httpx/tenacity in Python, native context propagation in Go, reqwest in Rust)

## Process / sequencing notes

- Build one full implementation (spec → API → connectors → passing contract tests) before starting the next language — sequential, not parallel, so ramp-up speed is provable via git history.
- Keep a `NOTES.md` per language, written *as you go*: what surprised you, which idiom took longest to click, day-1 vs day-3 differences. This is the actual evidence of rapid ramp-up — the code alone doesn't prove it.
- Track "days to first passing contract test" per language in the README comparison table.
- Potential crossover: this could feed the LinkedIn Posts project (one post per language) and possibly the Developer Pathway golden-path project later as a reference implementation — not required for v1, just worth keeping in mind structurally.

## Not yet decided (next steps once in Claude Code)

- Exact OpenAPI spec (endpoints/schema) for the issue tracker — not yet drafted, this is the immediate next task.
- Whether Rust actually makes the cut or stays a "maybe."
- CI matrix setup (GitHub Actions, path-scoped per language directory).
