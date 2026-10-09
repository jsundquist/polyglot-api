from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Label(SQLModel, table=True):
    __tablename__ = "labels" # type: ignore

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    name: str = Field(unique=True)
    color: str