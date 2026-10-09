
from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel

from polyglot.common.validators import NonEmptyText


class CommentRead(SQLModel):
    id: UUID
    issue_id: UUID
    author_id: UUID
    body: str
    created_at: datetime
    updated_at: datetime

class CommentCreate(SQLModel):
    body: NonEmptyText
    author_id: UUID

class CommentUpdate(SQLModel):
    body: NonEmptyText