from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import ARRAY, Column, Text
from sqlmodel import Field, SQLModel


class WebhookSubscription(SQLModel, table=True):
    __tablename__ = "webhook_subscriptions" # type: ignore

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    project_id: UUID = Field(foreign_key="projects.id")
    url: str
    events: list[str] = Field(sa_column=Column(ARRAY(Text), nullable=False))
    secret: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
