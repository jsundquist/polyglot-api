from datetime import datetime
from typing import Literal
from pydantic import field_validator
from sqlmodel import Field, SQLModel
from uuid import UUID

IssueStatus = Literal["open", "in-progress", "closed"]

class IssueRead(SQLModel):
    id: UUID
    project_id: UUID
    title: str
    description: str | None = None
    status: IssueStatus
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

class IssueUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    status: IssueStatus | None = None
    label_ids: list[UUID] | None = None
    assignee_ids: list[UUID] | None = None

    @field_validator("label_ids", "assignee_ids")
    @classmethod
    def dedupe(cls, ids: list[UUID] | None) -> list[UUID] | None:
        if ids is not None:
            return list(dict.fromkeys(ids))
        return ids

    @field_validator("title", "status")
    @classmethod
    def not_null(cls, v):
        if v is None:
            raise ValueError("Field cannot be null")
        return v
