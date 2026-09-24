# infra

Shared local dev infrastructure for polyglot-api. Currently: Postgres, managed via dbmate.

## Setup (one-time)

    brew install dbmate
    cp infra/.env.example infra/.env   # adjust if needed

## Bring up Postgres

    cd infra && docker compose up -d

## Run migrations

    cd infra && dbmate up

## New migration

    cd infra && dbmate new <name>

## Rollback last migration

    cd infra && dbmate down

## Notes

- dbmate owns the canonical schema for every language implementation. Each
  language's ORM (Prisma for TypeScript, etc.) only introspects/queries this
  schema — it should never run its own migrations against it.
- Redis is intentionally not included yet; add it here when a language
  implementation's connector work actually needs it.
