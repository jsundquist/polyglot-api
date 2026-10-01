from typing import Generic, TypeVar
from sqlmodel import SQLModel

T = TypeVar("T")

class Pagination(SQLModel):
    next_cursor: str | None = None
    limit: int

class Page(SQLModel, Generic[T]):
    items: list[T]
    pagination: Pagination