
from datetime import datetime
from sqlmodel import SQLModel
from uuid import UUID

from polyglot.common.validators import NonEmptyText

class CommentRead(SQLModel):
    id: UUID
    issue_id: UUID
    author_id: UUID
    body: str
    created_at: datetime
    updated_at: datetime

class CommentUpdate(SQLModel):
    body: NonEmptyText