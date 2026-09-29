"""
Property-based conformance testing against the shared OpenAPI contract.

Schemathesis generates requests for every operation in spec/spec.yaml and
checks that the server never errors (500) and that response bodies match
their documented schema. This catches contract drift that a hand-written
flow test wouldn't (undocumented fields, wrong types) even without
asserting on business-flow behavior - that's covered by test_lifecycle.py
instead.

This deliberately does NOT check status_code_conformance: the spec only
documents the "interesting" error responses per operation (401/404/409/422)
and doesn't enumerate every generic 400 a query/body validator can produce
(e.g. a malformed enum value). Fuzzing will legitimately hit those and they
aren't contract violations - just gaps in how exhaustively the spec
documents input validation. If you want to harden that, the fix is to add
those responses to spec/spec.yaml, not to loosen the implementation.

Note: the spec is OpenAPI 3.1; Schemathesis 3.x only has full support for
3.0, so it's loaded with force_schema_version="30" (3.1 is a superset of
3.0 for the features this spec uses, so this is safe here).
"""

import os
from pathlib import Path

import schemathesis

SPEC_PATH = Path(__file__).resolve().parent.parent / "spec" / "spec.yaml"
BASE_URL = os.environ.get("CONTRACT_TEST_BASE_URL", "http://localhost:8080/v1").rstrip("/")
API_KEY = os.environ.get("CONTRACT_TEST_API_KEY", "dev-local-key")

schema = schemathesis.from_path(
    str(SPEC_PATH),
    base_url=BASE_URL,
    force_schema_version="30",
)


@schema.parametrize()
def test_api_contract(case):
    case.headers = {**(case.headers or {}), "X-API-Key": API_KEY}
    case.call_and_validate(
        checks=(
            schemathesis.checks.not_a_server_error,
            schemathesis.checks.response_schema_conformance,
            schemathesis.checks.content_type_conformance,
        ),
    )
