from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class Label(SQLModel, table=True):
    __tablename__ = "labels" # type: ignore

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    name: str = Field(unique=True)
    color: str