from datetime import datetime
from enum import Enum
from pydantic import AnyHttpUrl, field_validator
from sqlmodel import Field, SQLModel
from uuid import UUID

class WebhookEvent(str, Enum):
    issue_created = "issue.created"
    issue_updated = "issue.updated"
    issue_status_changed = "issue.status_changed"

class WebhookRead(SQLModel):
    id: UUID
    project_id: UUID
    url: str
    events: list[WebhookEvent]
    created_at: datetime

class WebhookCreate(SQLModel):
    url: AnyHttpUrl
    events: list[WebhookEvent] = Field(min_length=1)
    secret: str | None = Field(default=None, min_length=1)

    @field_validator("events")
    @classmethod
    def dedupe_events(cls, events: list[WebhookEvent]) -> list[WebhookEvent]:
        return list(dict.fromkeys(events))
