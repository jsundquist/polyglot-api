
from sqlmodel import SQLModel
from uuid import UUID

class LabelRead(SQLModel):
    id: UUID
    name: str
    color: str

class LabelCreate(SQLModel):
    name: str
    color: str
