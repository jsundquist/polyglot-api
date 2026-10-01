from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
