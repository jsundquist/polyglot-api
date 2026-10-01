from datetime import datetime, timezone
from sqlalchemy import Column, Enum
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class Project(SQLModel, table=True):
    __tablename__ = "projects" # type: ignore

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    name: str
    key: str = Field(unique=True)
    description: str | None = None
    status: str = Field(
        default="active",
        sa_column=Column(
            Enum("active", "archived", name="project_status", create_type=False),
            nullable=False,
            server_default="active",
        ),
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
