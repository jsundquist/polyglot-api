from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Comment(SQLModel, table=True):
    __tablename__ = "comments" # type: ignore
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    issue_id: UUID
    author_id: UUID
    body: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))