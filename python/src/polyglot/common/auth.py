import os
import secrets

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

API_KEY = os.environ.get("POLYGLOT_API_KEY", "dev-local-key")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer = HTTPBearer(auto_error=False)

def require_api_key(
    api_key: str | None = Security(api_key_header),
    credentials: HTTPAuthorizationCredentials | None = Security(bearer),
):
    supplied = api_key or (credentials.credentials if credentials else None)
    if not supplied or not secrets.compare_digest(supplied, API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
