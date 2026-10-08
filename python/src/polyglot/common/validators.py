from typing import Annotated
from pydantic import AfterValidator, Field


def _no_null_bytes(v: str) -> str:
    if "\x00" in v:
        raise ValueError("must not contain null bytes")
    return v


SafeText = Annotated[str, AfterValidator(_no_null_bytes)]
NonEmptyText = Annotated[str, Field(min_length=1), AfterValidator(_no_null_bytes)]
