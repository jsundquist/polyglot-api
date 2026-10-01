from datetime import datetime, timezone

from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class Comment(SQLModel, table=True):
    __tablename__ = "comments" # type: ignore
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    issue_id: UUID
    author_id: UUID
    body: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))