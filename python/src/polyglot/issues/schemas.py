from datetime import datetime
from pydantic import field_validator
from sqlmodel import Field, SQLModel
from uuid import UUID

class IssueRead(SQLModel):
    id: UUID
    project_id: UUID
    title: str
    description: str | None = None
    status: str
    label_ids: list[UUID] = []
    assignee_ids: list[UUID] = []
    created_at: datetime
    updated_at: datetime

class IssueCreate(SQLModel):
    title: str = Field(min_length=1)
    description: str | None = None
    label_ids: list[UUID] = []
    assignee_ids: list[UUID] = []

    @field_validator("label_ids", "assignee_ids")
    @classmethod
    def dedupe(cls, ids: list[UUID]) -> list[UUID]:
        return list(dict.fromkeys(ids))

