from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from polyglot.comments.router import router as comments_router
from polyglot.common.auth import require_api_key
from polyglot.issues.router import router as issues_router
from polyglot.labels.router import router as labels_router
from polyglot.projects.router import router as projects_router
from polyglot.webhooks.router import router as webhooks_router

app = FastAPI()

api_v1 = APIRouter(prefix="/v1", dependencies=[Depends(require_api_key)])

api_v1.include_router(labels_router)
api_v1.include_router(projects_router)
api_v1.include_router(issues_router)
api_v1.include_router(comments_router)
api_v1.include_router(webhooks_router)

app.include_router(api_v1)

CODES = {
    401: "unauthorized",
    404: "not_found",
    405: "method_not_allowed",
    409: "conflict",
    422: "validation_error",
}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": CODES.get(exc.status_code),
            "message": exc.detail
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Path ids are opaque strings in the spec, so a malformed id is just "not found".
    if any(err["loc"][0] == "path" for err in exc.errors()):
        return JSONResponse(
            status_code=404,
            content={"code": "not_found", "message": "Resource not found"},
        )
    return JSONResponse(
        status_code=422,
        content={
            "code": "validation_error",
            "message": exc.errors()[0]["msg"],
            "details": {
                "errors": jsonable_encoder(exc.errors())
            }
        },
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}

