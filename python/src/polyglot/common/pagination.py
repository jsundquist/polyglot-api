from sqlmodel import SQLModel


class Pagination(SQLModel):
    next_cursor: str | None = None
    limit: int

class Page[T](SQLModel):
    items: list[T]
    pagination: Pagination