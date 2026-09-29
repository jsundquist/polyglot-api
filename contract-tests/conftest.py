import os
import uuid

import psycopg
import pytest
import requests
from hypothesis import HealthCheck, settings

BASE_URL = os.environ.get("CONTRACT_TEST_BASE_URL", "http://localhost:8080/v1").rstrip("/")
API_KEY = os.environ.get("CONTRACT_TEST_API_KEY", "dev-local-key")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgres://polyglot:polyglot@localhost:5432/polyglot_api?sslmode=disable",
)

# Bounds the schema-fuzzing suite (test_schema.py) so it stays fast and
# non-flaky both locally and in CI - this is a contract-conformance check,
# not an exhaustive fuzzer. Override with --hypothesis-profile=thorough for
# a deeper local run.
settings.register_profile("default", max_examples=25, deadline=None)
settings.register_profile(
    "thorough",
    max_examples=200,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "default"))


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def api_key() -> str:
    return API_KEY


@pytest.fixture(scope="session")
def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"X-API-Key": API_KEY, "Content-Type": "application/json"})
    return s


@pytest.fixture
def seeded_user() -> str:
    """
    The spec has no endpoint to create a `users` row - every implementation
    is expected to resolve identity from the API key out-of-band. Since all
    language implementations share the same Postgres instance (see /infra),
    we seed a real user row directly so tests can exercise author_id /
    assignee fields without depending on any one implementation's auth
    internals.
    """
    user_id = str(uuid.uuid4())
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (id) VALUES (%s)", (user_id,))
        conn.commit()
    return user_id
