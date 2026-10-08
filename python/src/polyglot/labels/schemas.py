
from sqlmodel import SQLModel
from uuid import UUID

from polyglot.common.validators import SafeText

class LabelRead(SQLModel):
    id: UUID
    name: str
    color: str

class LabelCreate(SQLModel):
    name: SafeText
    color: SafeText
