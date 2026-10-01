from datetime import datetime, timezone
from polyglot.users.models import User
from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4

from polyglot.labels.models import Label

class IssueLabel(SQLModel, table=True):
    __tablename__ = "issue_labels"  # type: ignore

    issue_id: UUID = Field(foreign_key="issues.id", primary_key=True)
    label_id: UUID = Field(foreign_key="labels.id", primary_key=True)


class IssueAssignee(SQLModel, table=True):
    __tablename__ = "issue_assignees"  # type: ignore

    issue_id: UUID = Field(foreign_key="issues.id", primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)

class Issue(SQLModel, table=True):
    __tablename__ = "issues" # type: ignore
    
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    project_id: UUID = Field(foreign_key="projects.id")
    title: str
    description: str | None = None
    status: str = Field(
        default="open",
        sa_column=Column(
            Enum("open", "in-progress", "closed", name="issue_status", create_type=False),
            nullable=False,
            server_default="open",
        ),
    )
    labels: list["Label"] = Relationship(link_model=IssueLabel)
    assignees: list["User"] = Relationship(link_model=IssueAssignee)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
